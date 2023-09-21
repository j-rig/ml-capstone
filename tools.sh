source_venv(){
  source ./build/venv/bin/activate;
}

setup_venv(){
  python3 -m venv ./build/venv;
  source ./build/venv/bin/activate;
  pip install wheel;
  pip install --upgrade -r ./dev.req.txt;
  pip install --compile -e ./src;
}

fmt_it(){
  echo "formating...";
  black src;
}

lint_it(){
  echo "linting...";
  pylint --exit-zero src;
}

build_notebook(){
  docker build -t ml-capstone-notebook -f notebook.Dockerfile .;
}

run_notebook(){
  cd ../;
  docker run -p 8888:8888 \
    --mount type=bind,source="$(pwd)"/ml-capstone,target=/app \
    ml-capstone-notebook jupyter notebook --allow-root --ip 0.0.0.0
}

build_webapp(){
  docker build -t ml-capstone-webapp -f webapp.Dockerfile .;
}

run_webapp(){
  docker run -p 5000:5000 \
    ml-capstone-webapp python3 /var/app/bizwiz/webapp.py;
}

run_webapp_venv(){
  python3 src/bizwiz/webapp.py;
}
