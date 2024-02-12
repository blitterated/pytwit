IMAGE_TAG=pytwit
CONTAINER_NAME=redfrik_pytwit

function container_exists () {
  [ -z "$(docker container inspect $CONTAINER_NAME 2>&1 1>/dev/null)" ]
  return $?
}
