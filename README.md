# AI Agent Backend

Bu proje, Flutter mobil uygulaması için AI destekli bir backend API'sidir. Farklı uzman sistemleri (expert systems) kullanarak kullanıcı sorularını yanıtlar.

## Özellikler

- Çoklu uzman sistemi (Spor, Yemek, AI, vb.)
- OpenAI entegrasyonu
- RESTful API endpoints
- CORS desteği
- Railway deployment desteği

## Kurulum

1. Repository'yi klonlayın:
```bash
git clone https://github.com/kadir49884/Ai_Agent_Backend.git
cd Ai_Agent_Backend
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. `.env` dosyasını oluşturun ve gerekli değişkenleri ekleyin:
```env
OPENAI_API_KEY=your_api_key_here
```

4. Uygulamayı başlatın:
```bash
python app.py
```

## API Endpoints

- `GET /health`: API sağlık kontrolü
- `POST /ask`: Soru sorma endpoint'i

### /ask Endpoint Kullanımı

```json
POST /ask
{
    "question": "Soru metni buraya"
}
```

## Railway Deployment

1. Railway.app üzerinden yeni proje oluşturun
2. GitHub repository'sini bağlayın
3. Environment variables'ları ayarlayın
4. Deploy edin

## Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın. 