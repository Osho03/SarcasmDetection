if True:
    from utils import reset_random, PandasDfToPyqtTable, Worker, plot_acc_loss, plot_cm_roc, get_measures, \
        print_measures_table

    reset_random()
import json
import os.path
import pickle
import sys

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QGroupBox, QGridLayout, QScrollArea, \
    QPushButton, QPlainTextEdit, QFrame, QTableView, QAbstractItemView, QLineEdit, QLabel, QSizePolicy
from keras.callbacks import ModelCheckpoint, Callback
from keras.utils import to_categorical

from cnn_rnn import cnn_rnn
from feature_engineering import get_tokenized_data, MAX_LENGTH, PADDING_TYPE, TRUNCATING_TYPE, get_glove_data, \
    EMBEDDING_DIM
from preprocess import preprocess_df, preprocess
from utils import clear_layout
from design import apply_design, add_glow, style_placeholder


def parse_data(path, log):
    log.emit('Loading Data From :: {0}'.format(path))
    with open(path, 'r') as file:
        for line in file.readlines():
            yield json.loads(line)


def json_to_df(json_path, log):
    json_data = list(parse_data(json_path, log))
    df = pd.DataFrame(pd.json_normalize(json_data), columns=['headline', 'is_sarcastic'])
    return df


class TrainingCallback(Callback):
    def __init__(self, acc_loss_csv_path_, acc_loss_graph_path_, log):
        self.acc_loss_csv_path = acc_loss_csv_path_
        self.acc_loss_graph_path_ = acc_loss_graph_path_
        self.log = log
        if os.path.isfile(self.acc_loss_csv_path):
            self.df = pd.read_csv(self.acc_loss_csv_path)
        else:
            self.df = pd.DataFrame([], columns=['epoch', 'accuracy', 'val_accuracy', 'loss', 'val_loss'])
            self.df.to_csv(self.acc_loss_csv_path, index=False)
        Callback.__init__(self)

    def on_epoch_end(self, epoch, logs=None):
        self.df.loc[len(self.df.index)] = [
            str(int(epoch + 1)).zfill(2), round(logs['accuracy'], 4), round(logs['val_accuracy'], 4),
            round(logs['loss'], 4), round(logs['val_loss'], 4)
        ]
        self.df.to_csv(self.acc_loss_csv_path, index=False)
        self.log('[EPOCH :: {0}] -> Acc :: {1} | Val_Acc :: {2} | Loss :: {3} | Val_Loss :: {4}'.format(
            *[self.df.values[-1][0]], *[str(v).ljust(6, '0') for v in self.df.values[-1][1:]])
        )
        plot_acc_loss(self.df, self.acc_loss_graph_path_)


class MainGUI(QWidget):
    def __init__(self):
        super(MainGUI, self).__init__()
        self.screen_size = app.primaryScreen().availableSize()
        self.app_width = self.screen_size.width()
        self.app_height = self.screen_size.height()
        self.setWindowTitle('Sarcasm Detection')
        self.setObjectName('MainGUI')
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.full_h_box = QHBoxLayout()
        self.full_h_box.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.left_v_box = QVBoxLayout()
        self.right_v_box = QVBoxLayout()

        self.gb_1 = QGroupBox('Input')
        self.gb_1.setFixedWidth((self.app_width // 100) * 49)
        self.gb_1.setFixedHeight((self.app_height // 100) * 20)
        self.grid_1 = QGridLayout()
        self.grid_1.setSpacing(20)
        self.gb_1.setLayout(self.grid_1)

        self.load_data_btn = QPushButton('Load Data')
        self.load_data_btn.clicked.connect(self.load_dataset_thread)
        self.grid_1.addWidget(self.load_data_btn, 0, 0)

        self.preprocess_btn = QPushButton('PreProcess')
        self.preprocess_btn.clicked.connect(self.preprocess_thread)
        self.grid_1.addWidget(self.preprocess_btn, 0, 1, 1, 2)

        self.fe_btn = QPushButton('Feature Engineering')
        self.fe_btn.clicked.connect(self.feature_engineering_thread)
        self.grid_1.addWidget(self.fe_btn, 1, 0)

        self.train_btn = QPushButton('Train CNN+RNN(LSTM) Network')
        self.train_btn.clicked.connect(self.train_cnn_rnn_lstm_thread)
        self.grid_1.addWidget(self.train_btn, 1, 1)

        self.reset_btn = QPushButton('Reset')
        self.reset_btn.clicked.connect(self.reset)
        self.grid_1.addWidget(self.reset_btn, 1, 2)

        self.gb_predict = QGroupBox('Test Your Own Headline')
        self.gb_predict.setFixedWidth((self.app_width // 100) * 49)
        self.gb_predict.setFixedHeight((self.app_height // 100) * 28)
        self.grid_predict = QGridLayout()
        self.grid_predict.setContentsMargins(14, 18, 14, 14)
        self.grid_predict.setHorizontalSpacing(12)
        self.grid_predict.setVerticalSpacing(10)
        self.gb_predict.setLayout(self.grid_predict)

        self.predict_edit = QLineEdit()
        self.predict_edit.setPlaceholderText(
            'Type a headline... e.g. "Bank patrons can expect same poor service after merger"')
        style_placeholder(self.predict_edit, '#67e8f9')
        add_glow(self.predict_edit, blur=12, alpha=110)
        self.predict_edit.returnPressed.connect(self.predict_thread)
        self.grid_predict.addWidget(self.predict_edit, 0, 0, 1, 3)

        self.predict_btn = QPushButton('Predict Sarcasm')
        self.predict_btn.setObjectName('primaryBtn')
        self.predict_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        add_glow(self.predict_btn, blur=10, alpha=100)
        self.predict_btn.clicked.connect(self.predict_thread)
        self.grid_predict.addWidget(self.predict_btn, 1, 0)

        self.predict_result = QLabel('Classify any headline instantly with the saved model.')
        self.predict_result.setWordWrap(True)
        self.predict_result.setAlignment(Qt.AlignCenter)
        self.predict_result.setObjectName('resultChip')
        self.grid_predict.addWidget(self.predict_result, 1, 1, 1, 2)
        self.grid_predict.setColumnStretch(0, 0)
        self.grid_predict.setColumnStretch(1, 1)
        self.grid_predict.setColumnStretch(2, 1)
        self.grid_predict.setRowStretch(1, 1)

        self.gb_2 = QGroupBox('Data')
        self.gb_2.setFixedWidth((self.app_width // 100) * 49)
        self.gb_2.setFixedHeight((self.app_height // 100) * 46)

        self.grid_2_scroll = QScrollArea()
        self.grid_2_scroll.setFrameShape(False)
        self.gb_2_v_box = QVBoxLayout()
        self.grid_2_widget = QWidget()
        self.grid_2_widget.hide()

        self.grid_2 = QGridLayout(self.grid_2_widget)
        self.gb_2.setLayout(self.gb_2_v_box)
        self.grid_2.setSpacing(20)
        self.grid_2_scroll.setWidgetResizable(True)
        self.grid_2_scroll.setWidget(self.grid_2_widget)
        self.gb_2_v_box.addWidget(self.grid_2_scroll)
        self.gb_2_v_box.setContentsMargins(0, 0, 0, 0)

        self.gb_3 = QGroupBox('Process')
        self.gb_3.setFixedWidth((self.app_width // 100) * 49)
        self.gb_3.setFixedHeight((self.app_height // 100) * 99)
        self.grid_3 = QGridLayout()
        self.grid_3.setSpacing(20)
        self.gb_3.setLayout(self.grid_3)

        self.process_pte = QPlainTextEdit()
        self.process_pte.setFont(QFont('JetBrains Mono', 10))
        self.process_pte.setStyleSheet('background-color: transparent;')
        self.process_pte.setReadOnly(True)
        self.process_pte.setFrameShape(QFrame.NoFrame)
        self.grid_3.addWidget(self.process_pte, 0, 1)

        self.full_h_box.addLayout(self.left_v_box)
        self.left_v_box.addWidget(self.gb_1)
        self.left_v_box.addWidget(self.gb_predict)
        self.left_v_box.addWidget(self.gb_2)
        self.full_h_box.addLayout(self.right_v_box)
        self.right_v_box.addWidget(self.gb_3)
        self.setLayout(self.full_h_box)

        self.source_df = None
        self.preprocessed_df = None
        self.train_df = None
        self.vocab_size = None
        self.embedding_matrix = None
        self.thread_pool = QThreadPool()

        self.showMaximized()

    def update_log(self, text):
        if isinstance(text, str):
            self.process_pte.appendPlainText('>>> {0}'.format(text))
        elif isinstance(text, tuple):
            self.process_pte.appendPlainText(text[0])

    def add_table(self, df):
        tableView = QTableView(self)
        model = PandasDfToPyqtTable(df)
        tableView.setFixedWidth((self.gb_2.width() // 100) * 100)
        tableView.setModel(model)
        tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableView.resizeColumnsToContents()
        self.grid_2.addWidget(tableView, self.grid_2.count() + 1, 0, Qt.AlignHCenter)

    def predict_thread(self):
        text = self.predict_edit.text().strip()
        if not text:
            self.predict_result.setText('<span style="color:#888888;">Type a headline first.</span>')
            return
        self.predict_btn.setEnabled(False)
        self.predict_result.setText('<span style="color:#888888;">Classifying...</span>')
        worker = Worker(self.predict_runner, text=text)
        worker.signals.finished.connect(self.predict_cleanup)
        worker.signals.result.connect(self.predict_finisher)
        worker.signals.error.connect(self.predict_error)
        self.thread_pool.start(worker)

    def predict_runner(self, text, log, table):
        from keras.models import load_model
        from keras.preprocessing.sequence import pad_sequences
        model_path = 'models/model.h5'
        tokenizer_path = 'Data/tokenizer.pkl'
        if not (os.path.isfile(model_path) and os.path.isfile(tokenizer_path)):
            return '<span style="color:#d9534f;">Model not found. Run Load Data > PreProcess > Feature Engineering > Train first.</span>'
        with open(tokenizer_path, 'rb') as f:
            tokenizer = pickle.load(f)
        cleaned = preprocess(text)
        if not isinstance(cleaned, str):
            return '<span style="color:#d9534f;">Cleaning removed every word. Try a longer headline.</span>'
        seq = tokenizer.texts_to_sequences([cleaned])
        x = pad_sequences(seq, maxlen=MAX_LENGTH, padding=PADDING_TYPE, truncating=TRUNCATING_TYPE)
        model = load_model(model_path)
        prob = model.predict(x, verbose=0)[0]
        idx = int(prob.argmax())
        confidence = prob[idx] * 100
        verdict = '<span style="color:#e67e22; font-weight:bold;">SARCASTIC</span>' if idx == 1 else \
            '<span style="color:#27ae60; font-weight:bold;">NOT SARCASTIC</span>'
        return '{0} &nbsp;|&nbsp; {1:.0f}% confidence'.format(verdict, confidence)

    def predict_finisher(self, result):
        self.predict_result.setText(result)

    def predict_cleanup(self):
        self.predict_btn.setEnabled(True)

    def predict_error(self, err):
        self.predict_result.setText('<span style="color:#d9534f;">Error: {0}</span>'.format(err[1]))

    def load_dataset_thread(self):
        self.reset()
        worker = Worker(self.load_dataset_runner)
        worker.signals.finished.connect(self.load_dataset_finisher)
        worker.signals.log_updater.connect(self.update_log)
        worker.signals.table_adder.connect(self.add_table)
        self.load_data_btn.setEnabled(False)
        self.thread_pool.start(worker)

    def load_dataset_runner(self, log, table):
        df1 = json_to_df('Data/source/Sarcasm_Headlines_Dataset.json', log)
        df2 = json_to_df('Data/source/Sarcasm_Headlines_Dataset_v2.json', log)
        log.emit('Concatenating DataFrames')
        df_ = pd.concat([df1, df2])
        log.emit('Data Shape :: {0}'.format(df_.shape))

        log.emit('Dropping Duplicates')
        df_.drop_duplicates(inplace=True)
        log.emit('Data Shape After Dropping Duplicates :: {0}'.format(df_.shape))

        data_save_path = 'Data/sarcasm.csv'
        log.emit('Saving Data :: {0}'.format(data_save_path))
        df_.to_csv(data_save_path, index=False)
        self.source_df = df_.copy(deep=True)

        log.emit('Data Loaded!')

    def load_dataset_finisher(self):
        self.preprocess_btn.setEnabled(True)
        self.add_table(self.source_df.head(100).copy())

    def preprocess_thread(self):
        worker = Worker(self.preprocess_runner)
        worker.signals.finished.connect(self.preprocess_finisher)
        worker.signals.log_updater.connect(self.update_log)
        worker.signals.table_adder.connect(self.add_table)
        self.thread_pool.start(worker)

    def preprocess_runner(self, log, table):
        df_ = preprocess_df(self.source_df.copy(), 'headline', log.emit)
        df_.dropna(inplace=True)
        df_.to_csv('Data/sarcasm_preprocessed.csv', index=False)
        self.preprocessed_df = df_.copy(deep=True)

    def preprocess_finisher(self):
        self.add_table(self.preprocessed_df.head(100).copy())
        self.preprocess_btn.setEnabled(False)
        self.fe_btn.setEnabled(True)

    def feature_engineering_thread(self):
        worker = Worker(self.feature_engineering_runner)
        worker.signals.finished.connect(self.feature_engineering_finisher)
        worker.signals.log_updater.connect(self.update_log)
        worker.signals.table_adder.connect(self.add_table)
        self.thread_pool.start(worker)

    def feature_engineering_runner(self, log, table):
        data = self.preprocessed_df['headline'].values
        labels = self.preprocessed_df['is_sarcastic'].values
        tokenized_data, word_indices = get_tokenized_data(data, log.emit)
        embedding_matrix = get_glove_data(word_indices, log.emit)
        self.vocab_size = len(word_indices)

        data_path = 'Data/sarcasm_training.csv'
        embedding_path = 'Data/glove_embedding_matrix.pkl'

        log.emit('Saving Data :: {0}'.format(data_path))
        train_df = pd.DataFrame(tokenized_data, columns=range(1, MAX_LENGTH + 1))
        train_df['Sarcastic'] = labels
        train_df.to_csv(data_path, index=False)
        self.train_df = train_df

        log.emit('Saving Glove Embedding Matrix :: {0}'.format(embedding_path))
        with open(embedding_path, 'wb') as f:
            pickle.dump(embedding_matrix, f)
        self.embedding_matrix = embedding_matrix

    def feature_engineering_finisher(self):
        self.fe_btn.setEnabled(False)
        self.train_btn.setEnabled(True)
        self.add_table(self.train_df.head(100).copy())

    def train_cnn_rnn_lstm_thread(self):
        worker = Worker(self.train_cnn_rnn_lstm_runner)
        worker.signals.finished.connect(self.train_cnn_rnn_lstm_finisher)
        worker.signals.log_updater.connect(self.update_log)
        worker.signals.table_adder.connect(self.add_table)
        self.thread_pool.start(worker)

    def train_cnn_rnn_lstm_runner(self, log, table):
        x_ = self.train_df.values[:, :-1]
        y_ = self.train_df.values[:, -1]

        log.emit('X Shape :: {0}'.format(x_.shape))
        log.emit('Splitting Data :: Train 80% / Validation 10% / Test 10%')
        x_train, x_test, y_train, y_test = train_test_split(
            x_, y_, test_size=0.2, random_state=42, stratify=y_)
        x_train, x_val, y_train, y_val = train_test_split(
            x_train, y_train, test_size=0.125, random_state=42, stratify=y_train)
        y_train_cat = to_categorical(y_train, num_classes=2)
        y_val_cat = to_categorical(y_val, num_classes=2)
        log.emit('Train Shape :: {0}'.format(x_train.shape))
        log.emit('Validation Shape :: {0}'.format(x_val.shape))
        log.emit('Test Shape :: {0}'.format(x_test.shape))

        model_dir = 'models'
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, 'model.h5')
        acc_loss_csv_path = os.path.join(model_dir, 'acc_loss.csv')
        acc_loss_graph_path = os.path.join(model_dir, '{0}')

        training_cb = TrainingCallback(acc_loss_csv_path, acc_loss_graph_path, log.emit)
        checkpoint = ModelCheckpoint(model_path, save_best_only=True,
                                     monitor='val_accuracy', mode='max', verbose=False)
        model = cnn_rnn(self.vocab_size, EMBEDDING_DIM, MAX_LENGTH, self.embedding_matrix, log.emit)
        initial_epoch = 0
        if os.path.isfile(model_path) and os.path.isfile(acc_loss_csv_path):
            log.emit('Loading Pre-Trained Model :: {0}'.format(model_path))
            model.load_weights(model_path)
            initial_epoch = len(pd.read_csv(acc_loss_csv_path))

        log.emit('Fitting Data')
        model.fit(x_train, y_train_cat, validation_data=(x_val, y_val_cat),
                  callbacks=[checkpoint, training_cb], batch_size=256,
                  epochs=10, initial_epoch=initial_epoch, verbose=0)

        log.emit('Evaluating On Held-Out Test Data')
        results_dir = 'results'
        os.makedirs(results_dir, exist_ok=True)
        model.load_weights(model_path)
        prob = model.predict(x_test)
        pred = np.argmax(prob, axis=1)
        plot_cm_roc(y_test, pred, prob, os.path.join(results_dir, '{0}'), log.emit)
        measure_names = ['Accuracy', 'Precision', 'Recall', 'F-Measure']
        df = pd.DataFrame([get_measures(y_test, pred, prob, log.emit)], columns=measure_names)
        print_measures_table(df, log.emit)
        df.to_csv(os.path.join(results_dir, 'measures.csv'), index=False)

    def train_cnn_rnn_lstm_finisher(self):
        self.train_btn.setEnabled(False)

    def disable(self):
        self.preprocess_btn.setEnabled(False)
        self.fe_btn.setEnabled(False)
        self.train_btn.setEnabled(False)
        self.load_data_btn.setEnabled(True)

    def reset(self):
        self.disable()
        clear_layout(self.grid_2)
        self.process_pte.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    apply_design(app)
    window = MainGUI()
    sys.exit(app.exec_())
