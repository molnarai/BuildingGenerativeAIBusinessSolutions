# N8N

## How to load an example workflow:
1. Download the JSON file
2. Create a new workflow
3. Select "Import from File..." from "..." menu in the upper right corner

![create workflow](image.png)

![import file](image-1.png)

## How to get the URL to my chat workflow:
1. Toggle switch on the upper right part of the window to "Active"
2. Open chat parameters and settings (double click on symbol)
3. The Chat URL is shown in the parameters tab; copy URL and open in another browser window or share with users.

![switch to active](image-2.png)

![confirm active](image-3.png)

![open chat settings](image-4.png)

![get chat url](image-5.png)

# n8n Experiments

## Quick Start

### Using Docker Compose

1. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

2. Set your admin password in `.env` or source it from your secrets:
   ```bash
   echo "ADMIN_PASSWORD=$(cat ~/.secrets/n8n-experiments-passwd.txt)" >> .env
   echo "UID=$(id -u)" >> .env
   echo "GID=$(id -g)" >> .env
   ```

3. Start the service:
   ```bash
   docker-compose up -d
   ```

4. Access n8n at http://localhost:23010

5. View logs:
   ```bash
   docker-compose logs -f
   ```

6. Stop the service:
   ```bash
   docker-compose down
   ```

### Using Launch Scripts

**Bash (Linux/Mac):**
```bash
./launch.sh start
./launch.sh stop
./launch.sh logs
```

**PowerShell (Windows/Mac/Linux):**
```powershell
./launch.ps1 start
./launch.ps1 stop
./launch.ps1 logs
```

## Configuration

- **Port**: Default is 23010 (configurable via CONSOLE_PORT)
- **Username**: admin
- **Password**: Stored in `~/.secrets/n8n-experiments-passwd.txt`
- **Data Directory**: `../n8n-experiments-data`
- **System Store**: `../n8n-experiments-system-store`

