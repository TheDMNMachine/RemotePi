#!/bin/bash
cd Desktop/RemoteControl
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 5000 --reload

