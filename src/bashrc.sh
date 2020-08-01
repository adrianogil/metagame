if [ -z "$METAGAME_PYTHON_PATH" ]
then
    export METAGAME_PYTHON_PATH=$METAGAME_DIR/python/
    export PYTHONPATH=$METAGAME_PYTHON_PATH:$PYTHONPATH
fi

alias metagame="python3 -m metagame"
