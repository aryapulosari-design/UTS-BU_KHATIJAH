from flask import Flask, render_template, request
import os

app = Flask(__name__)

# ====== SALIN DARI KODEMU: PriorityQueue, Graph, dan dijkstra() ======


# insertsion sort
class PriorityQueue:
    def __init__(self):
        self.items = []

    def push(self, kota, jarak):
        self.items.append((kota, jarak))
        for i in range(1, len(self.items)):
            key = self.items[i]
            j = i - 1
            while j >= 0 and self.items[j][1] > key[1]:
                self.items[j + 1] = self.items[j]
                j -= 1
            self.items[j + 1] = key

    def pop(self):
        if not self.items:
            return None
        return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0


class Graph:
    def __init__(self):
        self.graph = {}

    def tambah_kota(self, nama):
        if nama not in self.graph:
            self.graph[nama] = {}

    def tambah_jalur(self, kota1, kota2, jarak):
        self.tambah_kota(kota1)
        self.tambah_kota(kota2)
        self.graph[kota1][kota2] = jarak
        self.graph[kota2][kota1] = jarak


def dijkstra(graph, asal, tujuan):
    jarak = {kota: float('inf') for kota in graph}
    asal_kota = {kota: None for kota in graph}
    jarak[asal] = 0
    pq = PriorityQueue()
    pq.push(asal, 0)

    while not pq.is_empty():
        kota_sekarang, jarak_sekarang = pq.pop()
        if kota_sekarang == tujuan:
            break

        for tetangga, bobot in graph[kota_sekarang].items():
            total = jarak_sekarang + bobot
            if total < jarak[tetangga]:
                jarak[tetangga] = total
                asal_kota[tetangga] = kota_sekarang
                pq.push(tetangga, total)

    rute = []
    kota = tujuan
    while kota is not None:
        rute.insert(0, kota)
        kota = asal_kota[kota]
    return rute, jarak[tujuan]


# ====== DATA JALUR DEFAULT ======
peta = Graph()
jalur_default = [
    ("Lawang", "Singosari", 9), ("Singosari", "Karangploso", 8),
    ("Karangploso", "Malang", 10), ("Malang", "Lowokwaru", 6),
    ("Malang", "Sukun", 7), ("Lowokwaru", "Batu", 18),
    ("Batu", "Junrejo", 6), ("Batu", "Pujon", 14),
    ("Pujon", "Ngantang", 12), ("Ngantang", "Kasembon", 10),
    ("Sukun", "Turen", 16), ("Turen", "Dampit", 12),
    ("Dampit", "Ampelgading", 13), ("Ampelgading", "Gedangan", 9),
    ("Gedangan", "Bantur", 10), ("Bantur", "Sumbermanjing Wetan", 15),
    ("Sumbermanjing Wetan", "Dampit", 11), ("Malang", "Pakis", 9),
    ("Pakis", "Tumpang", 12), ("Tumpang", "Poncokusumo", 10),
    ("Poncokusumo", "Wajak", 9), ("Wajak", "Turen", 7)
]
for k1, k2, j in jalur_default:
    peta.tambah_jalur(k1, k2, j)

# ====== ROUTE WEB ======
@app.route('/')
def index():
    kota_list = list(peta.graph.keys())
    return render_template('index.html', kota_list=kota_list)

@app.route('/cari', methods=['POST'])
def cari():
    asal = request.form['asal']
    tujuan = request.form['tujuan']
    kecepatan = float(request.form['kecepatan'])

    rute, jarak = dijkstra(peta.graph, asal, tujuan)
    waktu = jarak / kecepatan if jarak != float('inf') else None
    return render_template('index.html',
                           kota_list=list(peta.graph.keys()),
                           hasil=True, rute=rute, jarak=jarak, waktu=waktu)

if __name__ == '__main__':
    app.run(debug=True)
