import os
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras import Sequential
import numpy as np
import pretty_midi

# 定义一些超参数
NUM_TIMESTEPS = 64
NUM_FEATURES = 128
BATCH_SIZE = 128
NUM_EPOCHS = 200

# 读取midi文件并将其转化为numpy数组
def midi_to_numpy(file_path):
    midi_data = pretty_midi.PrettyMIDI(file_path)
    piano_roll = midi_data.get_piano_roll(fs=4)
    piano_roll = piano_roll[:NUM_FEATURES, :]
    piano_roll[piano_roll > 0] = 1
    return piano_roll.T

# 创建训练数据和标签
def create_sequences(data, num_timesteps):
    sequences = []
    targets = []
    for i in range(num_timesteps, len(data)):
        sequences.append(data[i-num_timesteps:i])
        targets.append(data[i])
    return np.array(sequences), np.array(targets)

# 读取midi文件夹下的所有midi文件
def read_midi_files(midi_folder):
    all_data = []
    for root, dirs, files in os.walk(midi_folder):
        for file in files:
            if file.endswith(".midi") or file.endswith(".mid"):
                file_path = os.path.join(root, file)
                data

                data = midi_to_numpy(file_path)
                all_data.append(data)
    return np.vstack(all_data)

# 加载训练数据
midi_folder = "./maestro-v3.0.0/"
data = read_midi_files(midi_folder)

# 创建训练数据和标签
X, y = create_sequences(data, NUM_TIMESTEPS)

# 创建模型
model = Sequential([
    LSTM(256, input_shape=(NUM_TIMESTEPS, NUM_FEATURES), return_sequences=True),
    Dropout(0.2),
    LSTM(256),
    Dropout(0.2),
    Dense(NUM_FEATURES, activation='sigmoid')
])

# 编译模型
model.compile(optimizer='adam', loss='binary_crossentropy')

# 定义训练数据生成器，用于减少内存占用
def data_generator():
    while True:
        for i in range(0, len(X), BATCH_SIZE):
            yield X[i:i+BATCH_SIZE], y[i:i+BATCH_SIZE]

# 定义验证集
val_split = 0.1
val_size = int(len(X) * val_split)
val_X, val_y = X[-val_size:], y[-val_size:]
train_X, train_y = X[:-val_size], y[:-val_size]

# 训练模型并添加早停机制
early_stopping = tf.keras.callbacks.EarlyStopping(patience=10)
model.fit(data_generator(), steps_per_epoch=len(train_X)//BATCH_SIZE, epochs=NUM_EPOCHS,
          validation_data=(val_X, val_y), callbacks=[early_stopping])

# 保存模型
model.save('rnn_model.h5')

# 生成音乐
def generate_music(model, seed_sequence, num_timesteps):
    output_sequence = seed_sequence.copy()
    for i in range(num_timesteps):
        output = model.predict(np.expand_dims(output_sequence[-num_timesteps:], axis=0))
        output_sequence = np.vstack([output_sequence, output])
    return output_sequence

# 选择一个种子序列来生成音乐
seed_index = np.random.randint(0, len(data) - NUM_TIMESTEPS)
seed_sequence = data[seed_index:seed_index+NUM_TIMESTEPS]

# 生成音乐
generated_music = generate_music(model, seed_sequence, 128)

# 将生成的音乐写入midi文件
midi_data = pretty_midi.PrettyMIDI()
piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
piano = pretty_midi.Instrument(program=piano_program)
for i, note_sequence in enumerate(generated_music):
    for j, note in enumerate(note_sequence):
        if note > 0:
            note_start = int(j) / 4.0
            note_end = int(j + 1) / 4.0
            midi_note = pretty_midi.Note(
                velocity=int(100), pitch=int(i), start=note_start, end=note_end)
            piano.notes.append(midi_note)
midi_data.instruments.append(piano)
midi_data.write('generated_music.midi')
