#!/bin/bash

echo "버스 알림 시스템을 재시작합니다"
sudo systemctl daemon-reload
sudo systemctl restart uwsgi nginx
echo "완료되었습니다."

