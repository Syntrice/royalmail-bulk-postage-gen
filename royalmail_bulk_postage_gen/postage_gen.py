import pypdf, datetime

def read_orders(order_path: str) -> list[tuple[str, str, str]]:
    orders: list[tuple[str, str, str]] = []
    with open(order_path, "rb") as file:
        pdf = pypdf.PdfReader(file)
        for order in pdf.pages:
            order_text = order.extract_text()

            name_address = (
                order_text.split("Name & Address")[1]
                .split("Service Used")[0]
                .strip()
                .splitlines()
            )
            name = name_address[0]
            address = " ".join(name_address[1:])
            service = (
                order_text.split("Service Used")[1]
                .split("Official stamp:")[0]
                .strip()
                .splitlines()[0]
            )

            orders.append((name, address, service))

    return orders

def fill_order_form(order_data: list[tuple[str, str, str]], output_path: str = "output.pdf") -> None:
    with pypdf.PdfReader(bulk_postage_form_path) as reader, pypdf.PdfWriter() as writer:
        
        writer.clone_reader_document_root(reader)
        
        for i, (name, address, service) in enumerate(order_data):
            writer.update_page_form_field_values(writer.pages[0], {
                f"{i + 1}": name,
                f"address and postcode {i + 1}": address,
                f"service used {i + 1}": service,
            })
        
        with open(output_path, "wb") as file:
            writer.write(file)

if __name__ == "__main__":
    bulk_postage_form_path = "./resources/bulk_postage_form.pdf"
    orders_path = "./test/orders.pdf"
    output_path = f"./test/{datetime.datetime.today().strftime('%d-%m-%y')}.pdf"
    fill_order_form(read_orders(orders_path), output_path)
    
    