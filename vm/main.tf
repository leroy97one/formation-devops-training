resource "outscale_keypair" "keypair01" {
    keypair_name = "keypai-matteo"
}

resource "outscale_security_group" "matteo" {
    description         = "security group du M"
    security_group_name = "security group du M"
}

resource "outscale_security_group_rule" "security_group_rule01" {
    flow              = "Inbound"
    security_group_id = outscale_security_group.matteo.security_group_id
    from_port_range   = "22"
    to_port_range     = "22"
    ip_protocol       = "tcp"
    ip_range          = "0.0.0.0/0"
}

resource "outscale_security_group_rule" "security_group_rule02" {
    flow              = "Inbound"
    security_group_id = outscale_security_group.matteo.security_group_id
    from_port_range   = "443"
    to_port_range     = "443"
    ip_protocol       = "tcp"
    ip_range          = "0.0.0.0/0"
}


resource "outscale_vm" "demo" {
    image_id                 = "ami-1111f1b5"
    vm_type                  = "tinav4.c1r1p3"
    keypair_name             = outscale_keypair.keypair01.keypair_name
    security_group_ids       = [outscale_security_group.matteo.security_group_id]
     tags {
        key   = "Name"
        value = "terraform-public-vm"
    }
    
}

output"keypair"{
 value = outscale_keypair.keypair01.private_key
}

output"vm"{
 value = outscale_vm.demo.public_ip
}
