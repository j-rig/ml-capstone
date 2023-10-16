source_venv(){
  source ./build/venv/bin/activate;
}

setup_venv(){
  python3 -m venv ./build/venv;
  source ./build/venv/bin/activate;
  pip install wheel;
  pip install --compile -e ./src;
  pip install --upgrade -r ./dev.req.txt;
}

fmt_it(){
  echo "formating...";
  black src test blog;
}

lint_it(){
  echo "linting...";
  pylint --exit-zero src;
}

test_it(){
  echo "testing...";
  PYTHONPATH="$PWD/test" pytest test -o log_cli=true -o log_cli_level="INFO";
}

build_notebook(){
  docker build -t ml-capstone-notebook -f notebook.Dockerfile .;
}

run_notebook(){
  cd ../;
  docker run -p 8888:8888 \
    --mount type=bind,source="$(pwd)"/ml-capstone,target=/app \
    ml-capstone-notebook \
    jupyter notebook --allow-root --ip 0.0.0.0 \
      --NotebookApp.max_buffer_size=5000000000;
  cd ml-capstone;
}

run_spark_notebook(){
  cd ../;
  docker run -p 8888:8888 \
    --mount type=bind,source="$(pwd)"/ml-capstone,target=/home/jovyan/app \
    jupyter/pyspark-notebook;
  cd ml-capstone;
}

d_test_it(){
  cd ../;
  docker run \
    --mount type=bind,source="$(pwd)"/ml-capstone,target=/app \
    ml-capstone-webapp \
    python3 -mpytest /app/test;
  cd ml-capstone;
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

package_bizwiz(){
  fmt_it;
  test_it;
  cp blog/static/*.png src/bizwiz/static;
  python blog/proc_blog.py blog/blog.html > src/bizwiz/templates/blog.html;
  cd src/;
  python setup.py sdist;
  cd ../;
}
