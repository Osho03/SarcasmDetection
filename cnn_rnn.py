def cnn_rnn(vocab_size, embedding_dim, max_length, embedding_matrix, log):
    from keras.models import Sequential
    from keras.layers import (Embedding, Conv1D, MaxPooling1D, LSTM, Dense)
    from keras.optimizers import RMSprop
    lstm_out = 64
    model = Sequential(name='cnn_rnn')
    log('Building CNN+RNN(LSTM) Model')
    log('LSTM Out Unit :: {0}'.format(lstm_out))
    model.add(Embedding(vocab_size + 1, embedding_dim, input_length=max_length, weights=[embedding_matrix]))
    model.add(Conv1D(filters=128, kernel_size=3, padding='same', activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(LSTM(128, return_sequences=True))
    model.add(LSTM(lstm_out))
    model.add(Dense(16, activation='relu'), )
    model.add(Dense(2, activation='softmax'))
    optimizer = RMSprop(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    summary = []
    model.summary(print_fn=lambda s: summary.append(s))
    log('\n'.join(summary))
    return model
