#!/bin/bash
. /root/.bashrc

/usr/bin/svscan /etc/service/ &
sleep 4
su hduser -c"echo $ZOOKEEPER_ID > /var/zookeeper/myid"
su hduser -c ". /home/hduser/.bashrc; ssh -l hduser master1.gt 'bash -l -c \"zkServer.sh start\"'"
# su hduser -c ". /home/hduser/.bashrc; ssh -l hduser slave1.gt 'bash -l -c \"zkServer.sh start\"'"
# su hduser -c ". /home/hduser/.bashrc;; ssh -l hduser slave2.gt 'bash -l -c \"zkServer.sh start\"'"
if [ "$NODE_TYPE" = "m" ]; then
   su hduser -c ". /home/hduser/.bashrc; $HADOOP_INSTALL/sbin/start-dfs.sh"
   su hduser -c ". /home/hduser/.bashrc; $HADOOP_INSTALL/sbin/start-yarn.sh"
fi
sleep 4
su hduser -c ". /home/hduser/.bashrc; $ACCUMULO_HOME/bin/accumulo init --instance-name gis --password secret"
su hduser -c ". /home/hduser/.bashrc; hadoop fs -mkdir -p /accumulo/system-classpath/"
# su hduser -c ". /home/hduser/.bashrc; $ACCUMULO_HOME/bin/start-all.sh"
$ACCUMULO_HOME/bin/start-all.sh # weird accumulo logs workaround (happens on some docker settings)
su hduser -c ". /home/hduser/.bashrc; $SPARK_HOME/sbin/start-all.sh"
# tail -f $HADOOP_INSTALL/logs/*s
while true; do sleep 1; done
