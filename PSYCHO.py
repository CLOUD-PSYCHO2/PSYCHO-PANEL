import oci
import time

config = oci.config.from_file()
compute_client = oci.core.ComputeClient(config)

compartment_id = config["tenancy"]
availability_domain = "ap-singapore-2-AD-1" 
shape = "VM.Standard.A1.Flex"
subnet_id = "ocid1.subnet.oc1.ap-singapore-2.aaaaaaaahjzfhmd5clp3szw3cnlfivgnm3mfgpyxxghlilejj5k7bekmrwza" 
# সিঙ্গাপুর রিজিয়নের ওরাকল লিনাক্স (Oracle Linux) এআরএম ইমেজ আইডি
image_id = "ocid1.image.oc1.ap-singapore-2.aaaaaaaav7s76c37466l5l3m2k2j2h2g2f2d2s2a2p2o2i2u2y2t2r2e" 

def create_instance():
    while True:
        try:
            print("Trying to create Oracle Linux ARM Instance...")
            launch_details = oci.core.models.LaunchInstanceDetails(
                compartment_id=compartment_id,
                availability_domain=availability_domain,
                shape=shape,
                display_name="oracle-linux-arm-vm",
                shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
                    ocpus=4,
                    memory_in_gbs=24
                ),
                create_vnic_details=oci.core.models.CreateVnicDetails(
                    subnet_id=subnet_id,
                    assign_public_ip=True
                ),
                source_details=oci.core.models.InstanceSourceViaImageDetails(
                    image_id=image_id
                )
            )
            
            response = compute_client.launch_instance(launch_details)
            print("Instance created successfully!", response.data)
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Retrying in 90 seconds...")
            time.sleep(90)

if __name__ == "__main__":
    create_instance()
