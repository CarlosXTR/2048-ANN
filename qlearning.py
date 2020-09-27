import time

import numpy as np
from keras.layers import Dense, InputLayer
from keras.models import Sequential
from keras.optimizers import Adam


class Qlearning:

    def __init__(self, environment, learning_rate=0.1, discount=0.95, episodes=500) -> None:
        self.learning_rate = learning_rate
        self.discount = discount
        self.episodes = episodes
        self.env = environment
        self.n_actions_space = environment.n_actions_space
        self.model = None

        self.create_model()

    def deep_model(self):
        self.model = Sequential()
        self.model.add(InputLayer(batch_input_shape=(1, 16)))
        self.model.add(Dense(32, activation='sigmoid'))
        self.model.add(Dense(4, activation='linear'))
        self.model.compile(loss='mse', optimizer='adam', metrics=['mae'])

    def create_model(self):
        self.model = Sequential()
        self.model.add(InputLayer(batch_input_shape=(1, 16)))
        self.model.add(Dense(24, activation="relu"))
        self.model.add(Dense(48, activation="relu"))
        self.model.add(Dense(24, activation="relu"))
        self.model.add(Dense(self.n_actions_space))
        self.model.compile(loss="mean_squared_error",
            optimizer=Adam(lr=self.learning_rate))


    def start(self):
        y = 0.95
        eps = self.learning_rate
        decay_factor = self.discount
        r_avg_list = []

        print("Start Learning")
        for i in range(self.episodes):
            state = self.env.reset()
            eps *= decay_factor
            if i % 100 == 0:
                print(f"Episode {i+1} of {self.episodes}")
            done = False
            r_sum = 0

            while not done:

                if np.random.random_sample() < eps:
                    action = np.random.randint(0, self.env.n_actions_space)
                else:
                    action = np.argmax(self.model.predict(state))

                new_s, reward, done = self.env.step(action+1)
                #self.env.print()
                target = reward + y * np.max(self.model.predict(new_s))
                target_vec = self.model.predict(state)[0]
                target_vec[action] = target
                self.model.fit(state, target_vec.reshape(-1,
                                                         self.env.n_actions_space), epochs=1, verbose=0)

                state = new_s
                r_sum += reward

            print(f"Lost: {self.env.score}")
            print(self.env.table)
            r_avg_list.append(r_sum / 1000)
