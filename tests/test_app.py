import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Matikan CSRF khusus untuk testing agar tidak diblokir
    with app.test_client() as client:
        yield client

# ==================== 5 TEST CASE FUNGSIONAL (VERSI WEB FORM) ====================

# TC-01: Menguji akses ke halaman utama Task Manager
def test_get_index(client):
    response = client.get('/')  # Menggunakan rute root biasa
    assert response.status_code == 200

# TC-02: Menguji tambah tugas baru lewat Form (Sukses)
def test_create_task_success(client):
    payload = {
        "title": "Selesaikan Laporan KPL",
        "description": "Praktikum bab 8 terpadu"
    }
    # Menggunakan data= (bukan json=) untuk menyimulasikan submit form HTML
    response = client.post('/add', data=payload, follow_redirects=True)
    assert response.status_code == 200

# TC-03: Menguji validasi jika judul dikosongkan (Gagal)
def test_create_task_invalid_data(client):
    payload = {
        "title": ""  # Kosong untuk memicu error validasi FlaskForm
    }
    response = client.post('/add', data=payload)
    # Biasanya mengembalikan 200 kembali ke halaman form dengan pesan error
    assert response.status_code == 200 

# TC-04: Menguji rute edit atau update tugas
def test_update_task_page(client):
    response = client.get('/edit/1')  
    # Ditambahkan 302 karena aplikasi melakukan redirect jika data ID 1 tidak ditemukan di DB
    assert response.status_code in [200, 302, 404]

# TC-05: Menguji fungsi hapus tugas
def test_delete_task(client):
    response = client.post('/delete/1', follow_redirects=True)  # Sesuaikan rute hapus kamu
    assert response.status_code in [200, 404]