import oci
import time

config = oci.config.from_file()
compute_client = oci.core.ComputeClient(config)

compartment_id = config["tenancy"]
availability_domain = "ap-singapore-1-AD-1" # আপনার রিজিয়ন অনুযায়ী এডির নাম
shape = "VM.Standard.A1.Flex"
subnet_id = "ocid1.subnet.oc1.ap-singapore-2.aaaaaaaaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # আপনার সাবনেট আইডি এখানে বসাবেন
image_id = "ocid1.image.oc1.ap-singapore-2.aaaaaaaayyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy" # আপনার ডিস্ক ইমমেজ আইডি

def create_instance():
    while True:
        try:
            print("Trying to create ARM Instance...")
            launch_details = oci.core.models.LaunchInstanceDetails(
                compartment_id=compartment_id,
                availability_domain=availability_domain,
                shape=shape,
                display_name="free-arm-vm",
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
            print(f"Error (Out of capacity usually): {e}")
            print("Retrying in 5 minutes...")
            time.sleep(300)

if __name__ == "__main__":
    create_instance()
