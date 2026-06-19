from locust import HttpUser, task, between

class TaskManagerUser(HttpUser):
    # Waktu tunggu acak antara 1 hingga 3 detik antar aktivitas user
    wait_time = between(1, 3)

    @task(3)  # Angka 3 berarti tugas ini dijalankan 3x lebih sering (bobot lebih tinggi)
    def view_tasks(self):
        """Simulasi user membuka halaman utama untuk melihat daftar tugas"""
        self.client.get("/")

    @task(1)  # Bobot 1 (lebih jarang dibanding hanya melihat-lihat)
    def create_task(self):
        """Simulasi user mengisi form dan menambah tugas baru"""
        payload = {
            "title": "Tugas Otomatis Locust",
            "description": "Menguji beban concurrency server backend"
        }
        # Menggunakan data= untuk menyimulasikan submit form HTML tradisional
        self.client.post("/add", data=payload)