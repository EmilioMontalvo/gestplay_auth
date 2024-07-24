# Leer variables del archivo .env y almacenarlas en un hash table
$envVars = @{}
Get-Content .env | ForEach-Object {
    if ($_ -match "^(.*?)=(.*)$") {
        $name, $value = $matches[1], $matches[2]
        $envVars[$name] = $value
    }
}

# Verificar que las variables necesarias están presentes
if (-not $envVars.ContainsKey("DOCKER_USERNAME") -or -not $envVars.ContainsKey("DOCKER_PASSWORD")) {
    Write-Host "DOCKER_USERNAME or DOCKER_PASSWORD is not set in .env file. Exiting script."
    exit 1
}

$dockerUsername = $envVars["DOCKER_USERNAME"]
$dockerPassword = $envVars["DOCKER_PASSWORD"]
$imageName = "$dockerUsername/gestplay-backend:latest"

Write-Host "Login..."
try {
    docker login -u $dockerUsername -p $dockerPassword
    Write-Host "Login successful."
} catch {
    Write-Host "Login failed. Exiting script."
    exit 1
}

Write-Host "Building Docker image..."
try {
    docker-compose -f docker-compose-build.yaml build
    Write-Host "Docker image built successfully."
} catch {
    Write-Host "Failed to build Docker image. Exiting script."
    exit 1
}

Write-Host "Tagging Docker image..."
try {
    docker tag auth_service:latest $imageName
    Write-Host "Docker image tagged successfully."
} catch {
    Write-Host "Failed to tag Docker image. Exiting script."
    exit 1
}

# Verificar si la imagen se construyó y etiquetó correctamente
Write-Host "Verifying Docker image..."
try {
    docker image inspect $imageName
    Write-Host "Docker image exists locally."
} catch {
    Write-Host "Docker image does not exist locally. Exiting script."
    exit 1
}


Write-Host "Pushing Docker image..."
try {
    docker push $imageName
    Write-Host "Docker image pushed successfully."
} catch {
    Write-Host "Failed to push Docker image. Exiting script."
    exit 1
}

Write-Host "Pulling image for testing..."
try {
    docker-compose -f docker-compose-test.yaml up -d
    Write-Host "Docker image pulled successfully."
} catch {
    Write-Host "Failed to pull Docker image. Exiting script."
    exit 1
}


