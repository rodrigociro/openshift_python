import os
import subprocess

def login():
   os.system("oc login --token=OCP_TOKEN --server=URL_SERVER --insecure-skip-tls-verify=true")
   namespaces()

def namespaces():
   lista = []
   #Pasar el output de shellscript a una lista
   cmd="oc get namespaces --no-headers | grep stevo | awk '{print $1}'"
   projects = subprocess.Popen(cmd,shell=True,stdin=None,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   result=projects.stdout.readlines()

   if len(result) >= 1:
       for line in result:
           #Rellenar lista
           lista.append(line.decode("utf-8"))

   podStatus(lista)

def podStatus(lista):
   pod = []
   for lis in lista:
       os.system("oc project " + lis)
       #print('\033[92m'+"Namespace: " +lis+'\033[0m')
       cmd="oc get pods | awk '{print $3}' | grep -v STATUS |uniq -c"
       podstatus = subprocess.Popen(cmd,shell=True,stdin=None,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
       test=podstatus.stdout.readlines()

       #print(podstatus)

       if len(test) >= 1:
           for line in test:
               pod.append("namespace: " + lis + line.decode("utf-8"))


       #print(podstatus.decode('utf-8'))
   #print(pod)
   traza(pod)
def traza(pod):
    for p in pod:
        print('_________________________')
        if p.find('Running') != -1:
            print('\033[92m'+p+'\033[0m')
        else:
            print('\033[91m'+p+'\033[0m')

def main():
    login()

if __name__ == "__main__":
    main()
