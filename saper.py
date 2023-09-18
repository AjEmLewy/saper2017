# uncompyle6 version 3.9.0
# Python bytecode version base 3.4 (3310)
# Decompiled from: Python 3.6.8 (default, Jun 20 2023, 11:53:23) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: saper.py
from tkinter import *
from PIL.ImageTk import PhotoImage
import time, random, glob, os
files = glob.glob('Images/*.jpg')

class MainWindow:

    def __init__(self, root):
        self.images = self.load_images()
        self.root = root
        self.load_datas(10, 10, 10)
        self.make_menu()
        self.make_srodek_z_wyswietlaczem()
        self.make_przyciski()
        self.root.title('Saper')

    def load_images(self):
        meh = {}
        for file in files:
            name = os.path.split(file)[1]
            name = name.split('.')[0]
            meh[name] = PhotoImage(file=file)

        return meh

    def load_datas(self, lwr, lwk, lb):
        SaperButton.ile = 0
        SaperButton.the_game_is_on = False
        SaperButton.zaznaczone = set()
        self.czas = 0
        self.liczba_w_rzedzie = lwr
        self.liczba_w_kolumnie = lwk
        self.liczba_wszystkich = self.liczba_w_rzedzie * self.liczba_w_kolumnie
        self.liczba_bomb = lb
        self.ile_bomb_zostalo = lb
        self.zerowe = [x * self.liczba_w_rzedzie for x in range(self.liczba_w_kolumnie)]
        self.ostatnie = [self.liczba_w_rzedzie * (x + 1) - 1 for x in range(self.liczba_w_kolumnie)]
        self.gora = list(range(self.liczba_w_rzedzie))
        self.dol = [(self.liczba_w_kolumnie - 1) * self.liczba_w_rzedzie + x for x in range(self.liczba_w_rzedzie)]
        self.koniec = False

    def make_menu(self):
        meniu = Menu(self.root)
        self.root.config(menu=meniu)
        plik = Menu(meniu)
        plik.add_command(label='Rozdaj', command=self.od_nowa)
        self.trudnosc_var = StringVar()
        self.trudnosc_var.set('Easy')
        ustawienia = Menu(plik)
        ustawienia.add_radiobutton(label='Easy', variable=self.trudnosc_var, command=self.od_nowa)
        ustawienia.add_radiobutton(label='Medium', variable=self.trudnosc_var, command=self.od_nowa)
        ustawienia.add_radiobutton(label='Hard', variable=self.trudnosc_var, command=self.od_nowa)
        plik.add_cascade(label='Ustawienia', menu=ustawienia)
        plik.add_command(label='Najlepsze wyniki...', command=self.najlepsze_wyniki)
        plik.add_command(label='Koniec', command=self.root.quit)
        meniu.add_cascade(label='Plik', menu=plik)

    def make_srodek_z_wyswietlaczem(self):
        frm = Frame(self.root, relief=SUNKEN, bd=1, bg='beige')
        frm.pack(side=TOP, fill=X)
        czas_label = Label(frm, bg='beige', text='Czas :\t%03d' % self.czas)
        czas_label.pack(side=LEFT, anchor=W)
        self.czas_label = czas_label
        frm2 = Frame(frm, width=150, bg='beige', pady=2)
        frm2.pack(side=LEFT, fill=X, expand=YES)
        Button(frm2, image=self.images['start'], command=self.od_nowa).pack()
        self.ile_bomb = Label(frm, bg='beige', text='Bomb:\t %03d' % self.ile_bomb_zostalo)
        self.ile_bomb.pack(side=RIGHT)

    def make_przyciski(self):
        self.sprawdzone = set()
        self.rama_glowna = Frame(self.root, highlightthickness=0, bd=0)
        self.rama_glowna.pack(side=BOTTOM)
        self.czas_label.config(text='Czas :\t%03d' % self.czas)
        self.ile_bomb.config(text='Bomb:\t %03d' % self.ile_bomb_zostalo)
        self.miejsca_bomb = self.znajdz_miejsca_bomb()
        self.przyciski = []
        for i in range(self.liczba_w_kolumnie):
            frm = Frame(self.rama_glowna, highlightthickness=0, bd=0)
            frm.pack(side=TOP)
            for j in range(self.liczba_w_rzedzie):
                typ = self.okresl_typ_bomby(i * self.liczba_w_rzedzie + j)
                sb = SaperButton(frm, self.images, i * self.liczba_w_rzedzie + j, self)
                sb.ustal_typ(typ)
                sb.pack(side=LEFT)
                self.przyciski.append(sb)

    def od_nowa(self):
        self.rama_glowna.destroy()
        self.ustawienia()
        self.make_przyciski()

    def ustawienia(self):
        if self.trudnosc_var.get() == 'Easy':
            print('ez')
            self.load_datas(10, 10, 10)
        else:
            if self.trudnosc_var.get() == 'Medium':
                print('med')
                self.load_datas(16, 16, 40)
            elif self.trudnosc_var.get() == 'Hard':
                print('hard')
                self.load_datas(30, 16, 99)

    def najlepsze_wyniki(self):
        print('top level')

    def znajdz_miejsca_bomb(self):
        bomby = []
        while len(bomby) != self.liczba_bomb:
            a = random.randint(0, self.liczba_wszystkich - 1)
            if a not in bomby:
                bomby.append(a)
                continue

        return bomby

    def okresl_typ_bomby(self, pozycja):
        mb = self.miejsca_bomb
        typ = 0
        lwr = self.liczba_w_rzedzie
        if pozycja in mb:
            return 'bomba-off'
        if pozycja - lwr - 1 in mb:
            if pozycja not in self.zerowe:
                typ += 1
        if pozycja - lwr in mb:
            typ += 1
        if pozycja - lwr + 1 in mb:
            if pozycja not in self.ostatnie:
                typ += 1
        if pozycja - 1 in mb:
            if pozycja not in self.zerowe:
                typ += 1
        if pozycja + 1 in mb:
            if pozycja not in self.ostatnie:
                typ += 1
        if pozycja + lwr - 1 in mb:
            if pozycja not in self.zerowe:
                typ += 1
        if pozycja + lwr in mb:
            typ += 1
        if pozycja + lwr + 1 in mb:
            if pozycja not in self.ostatnie:
                typ += 1
        return str(typ)

    def sprawdz_otoczenie(self, numer):
        if numer not in self.gora:
            self.sprawdzone.add(numer)
            if numer - self.liczba_w_rzedzie not in self.sprawdzone:
                self.przyciski[numer - self.liczba_w_rzedzie].sprawdz()
            if numer not in self.dol:
                self.sprawdzone.add(numer)
                if numer + self.liczba_w_rzedzie not in self.sprawdzone:
                    self.przyciski[numer + self.liczba_w_rzedzie].sprawdz()
            if numer not in self.zerowe:
                if numer - 1 not in self.sprawdzone:
                    self.przyciski[numer - 1].sprawdz()
            if numer not in self.ostatnie:
                if numer + 1 not in self.sprawdzone:
                    self.przyciski[numer + 1].sprawdz()
            if numer not in self.gora:
                if numer not in self.zerowe:
                    if numer - self.liczba_w_rzedzie - 1 not in self.sprawdzone:
                        self.przyciski[numer - self.liczba_w_rzedzie - 1].sprawdz()
            if numer not in self.gora:
                if numer not in self.ostatnie:
                    if numer - self.liczba_w_rzedzie + 1 not in self.sprawdzone:
                        self.przyciski[numer - self.liczba_w_rzedzie + 1].sprawdz()
            if numer not in self.dol:
                if numer not in self.zerowe:
                    if numer + self.liczba_w_rzedzie - 1 not in self.sprawdzone:
                        self.przyciski[numer + self.liczba_w_rzedzie - 1].sprawdz()
            if numer not in self.dol:
                if numer not in self.ostatnie:
                    if numer + self.liczba_w_rzedzie + 1 not in self.sprawdzone:
                        self.przyciski[numer + self.liczba_w_rzedzie + 1].sprawdz()

    def przegrana(self, k):
        SaperButton.the_game_is_on = False
        for but in self.przyciski:
            but.config(state='disabled')

        for numex in self.miejsca_bomb:
            if numex != k and numex not in SaperButton.zaznaczone:
                self.przyciski[numex].config(image=self.images['bomba-off'])
                continue

        for butex in SaperButton.zaznaczone:
            if butex not in self.miejsca_bomb:
                self.przyciski[butex].config(image=self.images['zle'])
                continue

    def wygrana(self):
        SaperButton.the_game_is_on = False
        print(self.czas)
        for but in self.przyciski:
            but.config(state='disabled')

        for numex in self.miejsca_bomb:
            self.przyciski[numex].config(image=self.images['git'])

    def start_licznik(self):
        self.root.after(1000, self.wlasciwy_licznik)

    def wlasciwy_licznik(self):
        if SaperButton.the_game_is_on:
            self.czas += 1
            self.czas_label.config(text='Czas :\t%03d' % self.czas)
            self.root.after(1000, self.wlasciwy_licznik)


class SaperButton(Button):

    def __init__(self, parent, images, identyfikator, papa):
        self.im = images
        self.apka = papa
        self.choice = 0
        self.num = identyfikator
        Button.__init__(self, parent)
        self.config(image=self.im['0'], highlightthickness=0, bd=3)
        self.config(height=15, width=15, relief=RAISED)
        self.config(command=self.sprawdz)
        self.bind('<Button-3>', (lambda event: self.zmiana()))

    def zmiana(self):
        if self.choice == 0 and self['state'] != 'disabled' and self.apka.liczba_bomb != 0:
            self.choice = 1
            self.config(state='disabled')
            self.config(image=self.im['flaga'])
            self.apka.ile_bomb_zostalo -= 1
            self.apka.ile_bomb.config(text='Bomb:\t %03d' % self.apka.ile_bomb_zostalo)
            SaperButton.zaznaczone.add(self.num)
        elif self.choice == 1:
            if not self.apka.koniec:
                self.choice = 0
                self.config(state='normal')
                self.config(image=self.im['0'])
                self.apka.ile_bomb_zostalo += 1
                self.apka.ile_bomb.config(text='Bomb:\t %03d' % self.apka.ile_bomb_zostalo)
                SaperButton.zaznaczone.remove(self.num)

    def sprawdz(self):
        if self.choice == 0:
            if self.typ == 'bomba-off':
                self.config(image=self.im['bomba-on'], relief=SUNKEN)
                self.apka.koniec = True
                self.apka.przegrana(self.num)
        else:
            if not SaperButton.the_game_is_on:
                SaperButton.the_game_is_on = True
                self.apka.start_licznik()
            if self['state'] != 'disabled':
                SaperButton.ile += 1
                if SaperButton.ile == self.apka.liczba_wszystkich - self.apka.liczba_bomb:
                    self.koniec = True
                    self.apka.wygrana()
            self.config(state='disabled')
            self.config(image=self.im[self.typ])
            self.config(relief=SUNKEN)
            if self.typ == '0':
                self.apka.sprawdz_otoczenie(self.num)

    def ustal_typ(self, typ):
        self.typ = typ


if __name__ == '__main__':
    root = Tk()
    root.resizable(0, 0)
    k = MainWindow(root)
    root.mainloop()