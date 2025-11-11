# UMDM+ API Documentation

REST API documentation for backend integration.

## Base URL

```text
Development: http://localhost:3000/api
Production: https://api.umdm.app/v1
```

## Authentication

Most endpoints require JWT authentication.

```http
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Health Check

Check API status.

**GET** `/health`

**Response:**

```json
{
  "status": "ok",
  "timestamp": "2025-11-10T12:00:00Z",
  "uptime": 3600
}
```

---

### Get Supported Sites

List all supported platforms.

**GET** `/sites`

**Query Parameters:**

- `category` (optional): Filter by category (video, music, streaming, etc.)
- `search` (optional): Search by name

**Response:**

```json
{
  "total": 1100,
  "categories": {
    "video": ["YouTube", "TikTok", "Instagram"],
    "music": ["Spotify", "SoundCloud"],
    "streaming": ["Twitch", "Kick"]
  }
}
```

---

### Download Media

Queue a download.

**POST** `/download`

**Request Body:**

```json
{
  "url": "https://youtube.com/watch?v=example",
  "quality": "1080p",
  "format": "mp4",
  "audioOnly": false,
  "subtitles": true
}
```

**Response:**

```json
{
  "id": "download_123456789",
  "url": "https://youtube.com/watch?v=example",
  "status": "queued",
  "quality": "1080p",
  "format": "mp4",
  "estimatedTime": "2-5 minutes",
  "queuePosition": 3
}
```

---

### Get Download Status

Check download progress.

**GET** `/download/:id`

**Response:**

```json
{
  "id": "download_123456789",
  "status": "downloading",
  "progress": 45,
  "currentStep": "Extracting video stream",
  "speed": "2.5 MB/s",
  "eta": "2 minutes",
  "fileSize": "125 MB"
}
```

**Status values:**

- `queued` - Waiting in queue
- `downloading` - Actively downloading
- `processing` - Converting/processing
- `completed` - Ready to download
- `failed` - Error occurred

---

### Cancel Download

Cancel a queued or active download.

**DELETE** `/download/:id`

**Response:**

```json
{
  "success": true,
  "message": "Download cancelled"
}
```

---

### List Downloads

Get user's download history.

**GET** `/downloads`

**Query Parameters:**

- `page` (default: 1): Page number
- `limit` (default: 20): Items per page
- `status` (optional): Filter by status

**Response:**

```json
{
  "downloads": [
    {
      "id": "download_123456789",
      "url": "https://youtube.com/watch?v=example",
      "title": "Example Video",
      "status": "completed",
      "createdAt": "2025-11-10T10:00:00Z",
      "completedAt": "2025-11-10T10:05:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

---

### Convert Media

Convert media to different format.

**POST** `/convert`

**Request Body:**

```json
{
  "fileId": "download_123456789",
  "targetFormat": "mp3",
  "quality": "320k",
  "trimStart": "00:00:10",
  "trimEnd": "00:05:00"
}
```

**Response:**

```json
{
  "id": "convert_987654321",
  "fileId": "download_123456789",
  "targetFormat": "mp3",
  "status": "queued",
  "estimatedTime": "1-3 minutes"
}
```

---

### AI Transcription

Transcribe audio from video.

**POST** `/ai/transcribe`

**Request Body:**

```json
{
  "fileId": "download_123456789",
  "language": "en",
  "format": "srt"
}
```

**Response:**

```json
{
  "id": "transcribe_111222333",
  "fileId": "download_123456789",
  "status": "processing",
  "language": "en",
  "estimatedTime": "3-10 minutes"
}
```

---

### AI Summarization

Generate AI summary of video content.

**POST** `/ai/summarize`

**Request Body:**

```json
{
  "fileId": "download_123456789",
  "length": "brief"
}
```

**Response:**

```json
{
  "id": "summarize_444555666",
  "summary": "This video discusses...",
  "keyPoints": [
    "Point 1",
    "Point 2"
  ],
  "duration": "15:30",
  "topics": ["technology", "tutorial"]
}
```

---

### Video Upscaling

Upscale video resolution using AI.

**POST** `/ai/upscale`

**Request Body:**

```json
{
  "fileId": "download_123456789",
  "targetResolution": "4K",
  "model": "realesrgan"
}
```

**Response:**

```json
{
  "id": "upscale_777888999",
  "fileId": "download_123456789",
  "status": "queued",
  "targetResolution": "4K",
  "estimatedTime": "30-60 minutes"
}
```

---

### User Settings

Get/update user preferences.

**GET** `/settings`

**Response:**

```json
{
  "theme": "dark",
  "defaultQuality": "1080p",
  "defaultFormat": "mp4",
  "autoDownload": false,
  "notifications": true,
  "clipboardMonitor": true
}
```

**PUT** `/settings`

**Request Body:**

```json
{
  "theme": "dark",
  "defaultQuality": "1080p"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional info"
  }
}
```

**Common Status Codes:**

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error

---

## Rate Limiting

- **Authenticated users:** 100 requests per hour
- **Anonymous users:** 20 requests per hour

Rate limit headers:

```text
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1699632000
```

---

## WebSocket Events

Real-time updates via WebSocket connection.

**Connect:**

```javascript
const ws = new WebSocket('ws://localhost:3000/ws');
```

**Events:**

```javascript
// Download progress
{
  "event": "download:progress",
  "data": {
    "id": "download_123",
    "progress": 45,
    "speed": "2.5 MB/s"
  }
}

// Download complete
{
  "event": "download:complete",
  "data": {
    "id": "download_123",
    "downloadUrl": "/files/abc123.mp4"
  }
}

// Error
{
  "event": "download:error",
  "data": {
    "id": "download_123",
    "error": "Failed to download"
  }
}
```

---

## Pagination

List endpoints support pagination:

**Query Parameters:**

- `page` - Page number (default: 1)
- `limit` - Items per page (max: 100, default: 20)

**Response includes:**

```json
{
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

---

## Examples

### cURL Examples

**Download a video:**

```bash
curl -X POST http://localhost:3000/api/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://youtube.com/watch?v=example",
    "quality": "1080p",
    "format": "mp4"
  }'
```

**Check status:**

```bash
curl http://localhost:3000/api/download/download_123456789
```

### JavaScript Examples

**Using fetch:**

```javascript
// Download
const response = await fetch('http://localhost:3000/api/download', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    url: 'https://youtube.com/watch?v=example',
    quality: '1080p',
    format: 'mp4'
  })
});

const data = await response.json();
console.log(data.id); // download_123456789

// Check status
const statusResponse = await fetch(`http://localhost:3000/api/download/${data.id}`);
const status = await statusResponse.json();
console.log(status.progress); // 45
```

---

## SDK (Coming Soon)

Official SDKs planned:

- JavaScript/TypeScript
- Python
- Go
- Java

---

## Support

For API support, visit:

- Documentation: <https://docs.umdm.app>
- Discord: <https://discord.gg/umdm>
- GitHub Issues: <https://github.com/umdm/umdm-plus/issues>
