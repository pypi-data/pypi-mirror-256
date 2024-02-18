from discobiscuit import Client

__VERSION__ = "0.2.0"


def main():
    # INIT CLIENT
    protocol = "http"
    host = "eeel121"
    port = 21020

    client = Client(protocol=protocol, host=host, port=port)

    # DATA
    sfc = "THT_AOI_TEST_2024"
    operation_name = "SAOI"
    resource_name = "THT_AOI_TEST"

    # GET PRODUCT BY SFC
    response = client.mes.queries.get_product_by_sfc(sfc)
    if response.error:
        print(response.error)
    else:
        product = response.result
        dump = product.model_dump()

    # LOGIN
    print("Before login")
    print(f"Is client authenticated: {client.authenticated}")

    # Attempting authentication with false credentials
    non_existing_user = "test_user_false"
    invalid_password = "00000000"
    response = client.login(non_existing_user, invalid_password)
    if response.error:
        print(response.error)

    username = "test_user"
    password = "12345678"
    response = client.login(username=username, password=password)
    print("After login")
    print(f"Is client authenticated: {client.authenticated}")

    # START OPERATION
    response = client.mes.commands.start_operation(
        sfc=sfc, operation_name=operation_name, resource_name=resource_name
    )
    print(f"Start response: {response}")

    # COMPLETE OPERATION
    response = client.mes.commands.complete_operation(
        sfc=sfc, operation_name=operation_name, resource_name=resource_name
    )
    print(f"Complete response: {response}")

    # LOGOUT
    client.logout()
    print("After logout")
    print(f"Is client authenticated: {client.authenticated}")


if __name__ == "__main__":
    main()
