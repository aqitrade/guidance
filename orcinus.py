#!/usr/bin/env python3

import os, sys
import docker

algo_port = ''
algo_id = ''
algo_log_path = '/algo/algo/strategy/logs'
user = ''
devops_path = ''
extra_host = ''
host_name = ''
client = ''

def start():
  algo_name = 'algo_' + algo_port
  algo = client.containers.run(image='aqitrade/algo', name=algo_name, \
    ports={'8000/tcp': algo_port}, user=user, \
    volumes={devops_path+'/log/algo/'+algo_name: {'bind': algo_log_path, 'mode': 'rw'}}, \
    extra_hosts={'dockerhost': extra_host}, hostname=algo_name, \
    environment=['host_name='+host_name], detach=True)
  print('orcinus.start() [algo_id: {}]'.format(algo.id))

def stop_remove_by_id():
  containers = client.containers.list(all=True)

  ifFound = False
  for container in containers:
    if container.id == algo_id or container.id.startswith(algo_id):
      print('orcinus.stop_remove_by_id() [algo_id: {}]'.format(algo_id))
      container.stop()
      container.remove()
      ifFound = True
      break

  if ifFound == False:
    raise BaseException(logsHelper.error_text('algo container with id [{}] not found'.format(algo_id)))

def stop_remove_by_name():
  algo_name = 'algo_' + algo_port
  containers = client.containers.list(all=True)

  ifFound = False
  for container in containers:
    if container.name == algo_name:
      print('orcinus.stop_remove_by_name() [algo_name: {}]'.format(algo_name))
      container.stop()
      container.remove()
      ifFound = True
      break

  if ifFound == False:
    raise BaseException(logsHelper.error_text('algo container with name [{}] not found'.format(algo_name)))


# =+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
def orcinus():
  global algo_port
  global algo_id
  global user
  global devops_path
  global extra_host
  global host_name
  global client

  args = sys.argv
  action = args[1]

  client = docker.from_env()
  client.ping()

  if action == 'start':
    algo_port = args[2]
    user = args[3]
    devops_path = args[4]
    extra_host = args[5]
    host_name = args[6]
    start()
  elif action == 'stop_remove_by_id':
    algo_id = args[2]
    stop_remove_by_id()
  elif action == 'stop_remove_by_name':
    algo_port = args[2]
    stop_remove_by_name()
  else:
    raise BaseException(logsHelper.error_text('Unkown action [{}], choose among [start | stop_remove_by_id | stop_remove_by_name]'.format(action)))


if __name__ == '__main__':
  orcinus()
