#/bin/bash
docker build . -t mail  && docker run -v MAIL:/app -it mail && docker update --restart unless-stopped mail
