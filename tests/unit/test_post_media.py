import os
from fastapi.testclient import TestClient
from conftest import images_dir


def test_post_media(test_client):    
    image_files = [f for f in os.listdir(images_dir)]
    
    for image_file in image_files:
        file_path = os.path.join(images_dir, image_file)
        
        with open(file_path, "rb") as file:
            file_data = ("test_file", file, "image/jpeg")
            
            response = test_client.post("/api/medias", files={"file": file_data})
            
            assert response.status_code == 200
            assert "media_id" in response.json()
