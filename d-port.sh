for port in 3141 5000 9000
do
    VBoxManage controlvm "default" natpf1 "tcp-port$port,tcp,127.0.0.1,$port,,$port"; echo
        $port
done
