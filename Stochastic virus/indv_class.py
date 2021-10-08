import random as rnd

def rnd_sign():
    return 1 if rnd.random() < 0.5 else -1



class Indv:         # Definicion de un individuo

    def __init__(self ,step_size, r_infec, p_infec, p_market, box, tmax_infec ,tmax_market):
        self.box = box                     # Tamapo de la region box x box

        self.x = self.box * (2 * rnd.random() - 1)          # Coordenadas iniciales
        self.y = self.box * (2 * rnd.random() - 1)

        self.step_size = step_size  # Tamaño del paso
        self.r_infec = r_infec  # Radio de infeccion
        self.p_infec = p_infec  # Probabilidad de infeccion
        self.p_market = p_market  # Probabilidad de ir al mercado

        self.tmax_infec = tmax_infec  # Tiempo de duracion de la infeccion
        self.tmax_market = tmax_market  # Tiempo en el mercado(?)

        self.est = 'S'            # Estado S-> suceptible, I-> infectado, R-> removido
        self.xcp, ycp = 0, 0      # Coordenadas auxiliares
        self.t = 0
        self.t_market = 0  # Tiempo en el mercado

    def rand_walk(self):  # Caminata aleatoria
        if self.est == 'I':
            self.t += 1  # Contador de tiempo infectado
        if self.t == self.tmax_infec:
            self.est = 'R'  # El individuo se cura
        random_sign_x = rnd_sign()
        random_sign_y = rnd_sign()
        self.x += self.step_size * random_sign_x
        self.y += self.step_size * random_sign_y
        if abs(self.x) >= self.box:
            self.x += 2 * self.step_size * (- 1 *random_sign_x)
        if abs(self.y) >= self.box:
            self.y += 2 * self.step_size * (- 1 *random_sign_y)


    def walk_market(self):  # Caminata aleatoria pero existe la probabilidad de que
        # el individuo visite un "mercado", que es un foco de infeccion
        if rnd.random() <= self.p_market and self.t_market == 0:
            self.xcp, self.ycp = self.x, self.y
            self.x, self.y = 0, 0
            self.t_market += 1
        elif self.t_market < self.tmax_market and self.t_market != 0:
            self.t_market += 1
        elif self.t_market == self.tmax_market:
            self.x, self.y = self.xcp, self.ycp
            self.t_market = 0
        else:
            if self.est == 'I':
                self.t += 1
            if self.t == self.tmax_infec:
                self.est = 'R'
            random_sign_x = rnd_sign()
            random_sign_y = rnd_sign()
            self.x += self.step_size * random_sign_x
            self.y += self.step_size * random_sign_y
            if abs(self.x) >= self.box:
                self.x += 2 * self.step_size * (- 1 *random_sign_x)
            if abs(self.y) >= self.box:
                self.y += 2 * self.step_size * (- 1 *random_sign_y)