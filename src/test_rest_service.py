#!flask/bin/python
import rest_service
import vpn_switcher

vpn_switcher.vpn_configs = [
                            {'in_channel':1,'out_channel':2,'country':'DE','config_id':'CG_DE'},
                            {'in_channel':3,'out_channel':4,'country':'US','config_id':'CG_US'}
                            ]
                            
rest_service.app.run(debug=True)
