export PATH="${PATH}:/opt/render/project/.render/chrome/opt/google/chrome"

gunicorn app:server -t 240 --keep-alive 240