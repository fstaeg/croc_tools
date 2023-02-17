for script in probecard_readout.py mux_vdd.py mux_needle_plotting.py root_plotting.py
  do 
    if ! [ -x $script ]
      then chmod +x $script
    fi
  done

export PATH=$PWD:$PATH