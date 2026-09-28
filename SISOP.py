# Simulasi Penjadwalan CPU: SJF Non-Preemptive dan Round Robin
# Data proses: (nama, arrival time, burst time)

proses = [
    ("P1", 0, 8),
    ("P2", 1, 3),
    ("P3", 2, 6),
    ("P4", 3, 2),
    ("P5", 4, 5),
]

QUANTUM = 3  # jatah waktu untuk Round Robin


def sjf_non_preemptive(data):
    waktu = 0
    belum_jalan = list(data)
    selesai = {}   # nama -> completion time
    gantt = []     # (nama, mulai, selesai)

    while belum_jalan:
        # cari proses yang sudah datang
        siap = [p for p in belum_jalan if p[1] <= waktu]

        # kalau belum ada yang datang, loncat ke waktu kedatangan berikutnya
        if not siap:
            waktu = min(p[1] for p in belum_jalan)
            continue

        # pilih burst time paling kecil
        nama, at, bt = min(siap, key=lambda p: p[2])

        # jalankan sampai selesai (tidak boleh disela)
        gantt.append((nama, waktu, waktu + bt))
        waktu += bt
        selesai[nama] = waktu
        belum_jalan.remove((nama, at, bt))

    return selesai, gantt


def round_robin(data, q):
    data = sorted(data, key=lambda p: p[1])  # urutkan berdasarkan arrival time
    sisa = {nama: bt for nama, at, bt in data}  # sisa waktu tiap proses
    antrean = []
    selesai = {}
    gantt = []
    waktu = 0
    i = 0  # penunjuk proses berikutnya yang belum masuk antrean

    while len(selesai) < len(data):
        # masukkan proses yang sudah datang ke antrean
        while i < len(data) and data[i][1] <= waktu:
            antrean.append(data[i][0])
            i += 1

        # kalau antrean kosong, loncat ke kedatangan berikutnya
        if not antrean:
            waktu = data[i][1]
            continue

        nama = antrean.pop(0)          # ambil dari depan antrean
        jalan = min(q, sisa[nama])     # jalan maksimal sebesar quantum
        gantt.append((nama, waktu, waktu + jalan))
        waktu += jalan
        sisa[nama] -= jalan

        # proses yang datang selama ini masuk antrean lebih dulu
        while i < len(data) and data[i][1] <= waktu:
            antrean.append(data[i][0])
            i += 1

        if sisa[nama] > 0:
            antrean.append(nama)       # belum selesai -> antre lagi di belakang
        else:
            selesai[nama] = waktu      # sudah selesai

    return selesai, gantt


def tampilkan(judul, data, selesai, gantt):
    print("=" * 50)
    print(judul)
    print("=" * 50)

    # Gantt chart
    print("Gantt Chart:")
    print(" -> ".join(f"{n}({m}-{s})" for n, m, s in gantt))
    print()

    print(f"{'Proses':<8}{'AT':<5}{'BT':<5}{'CT':<5}{'TAT':<6}{'WT':<5}")
    total_wt = 0
    total_tat = 0
    for nama, at, bt in data:
        ct = selesai[nama]
        tat = ct - at      # Turnaround Time = CT - AT
        wt = tat - bt      # Waiting Time = TAT - BT
        total_wt += wt
        total_tat += tat
        print(f"{nama:<8}{at:<5}{bt:<5}{ct:<5}{tat:<6}{wt:<5}")

    n = len(data)
    print()
    print(f"AWT  (rata-rata waktu tunggu) = {total_wt / n:.1f} ms")
    print(f"ATAT (rata-rata waktu putar)  = {total_tat / n:.1f} ms")
    print()


# ----- Jalankan kedua algoritma -----
selesai, gantt = sjf_non_preemptive(proses)
tampilkan("SJF Non-Preemptive", proses, selesai, gantt)

selesai, gantt = round_robin(proses, QUANTUM)
tampilkan(f"Round Robin (q = {QUANTUM} ms)", proses, selesai, gantt)