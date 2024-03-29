osxphotos query \
    --keyword CheckDate \
    --field uuid "{uuid}" \
    --field name "{original_name}" \
    --field type "{photo_or_video}" \
    --field created "{created.strftime,%Y-%m-%d %H:%M:%S}" \
    --field modified "{modified.strftime,%Y-%m-%d %H:%M:%S}" \
    --field camera_make {exif.camera_make} \
    --field camera_model {exif.camera_model} \
    --field album {album} \
    --field folder_album {folder_album} \
    --json > ./data/myphotos.json
