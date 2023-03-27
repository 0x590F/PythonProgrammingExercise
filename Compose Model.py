import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras import Sequential
import numpy as np
import pretty_midi

# 定义一些超参数
NUM_TIMESTEPS = 32
NUM_FEATURES = 128
BATCH_SIZE = 64
NUM_EPOCHS = 100

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
    LSTM(128, input_shape=(NUM_TIMESTEPS, NUM_FEATURES), return_sequences=True),
    LSTM(128),
    Dense(NUM_FEATURES, activation='sigmoid')
])

# 编译模型
model.compile(optimizer='adam', loss='binary_crossentropy')

# 训练模型
model.fit(X, y, batch_size=BATCH_SIZE, epochs=NUM_EPOCHS)

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
            note_start = i/4.0
            note_end = (i+1)/4.0
            note_pitch = j
            note_velocity = int(note*127)
            midi_note = pretty_midi.Note(
                velocity=note_velocity, pitch=note_pitch,duration=note_end - note_start, start=note_start)
piano.notes.append(midi_note)
midi_data.instruments.append(piano)
midi_data.write('generated_music.mid')
midi_data.instruments.append(piano)
midi_file_name = 'generated_music.mid'
midi_data.write(midi_file_name)
print(f"生成的midi文件已保存至 {midi_file_name}")
