import os
import csv
import html

class PriceMachine:
    def __init__(self):
        self.data = []

    def load_prices(self, file_path=''):
        for filename in os.listdir(file_path):
            if 'price' in filename:
                filepath = os.path.join(file_path, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f, delimiter=',')
                    headers = next(reader)
                    product_index = None
                    price_index = None
                    weight_index = None
                    for i, header in enumerate(headers):
                        if header.lower() in ('название', 'продукт', 'товар', 'наименование'):
                            product_index = i
                        elif header.lower() in ('цена', 'розница',):
                            price_index = i
                        elif header.lower() in ('фасовка', 'масса', 'вес'):
                            weight_index = i
                    if product_index is not None and price_index is not None and weight_index is not None:
                        for row in reader:
                            self.data.append({
                                'product': row[product_index].strip(),
                                'price': float(row[price_index].replace(',', '.').strip()),
                                'weight': float(row[weight_index].replace(',', '.').strip()),
                                'file': filename
                            })
                    else:
                        print(f"Файл {filename} не содержит необходимых колонок для поиска.")

    def find_products(self, search_term):

        results = [item for item in self.data if search_term.lower() in item['product'].lower()]


        results.sort(key=lambda item: item['price'] / item['weight'])
        return results

    def print_results(self, results):

        if results:
            print("-" * 80)
            print("Найденные товары:")
            print("-" * 80)
            print(f"{'Название':<30} {'Цена':<10} {'Вес (кг)':<10} {'Цена/кг':<10} {'Файл':<20}")
            print("-" * 80)
            for i, item in enumerate(results, start=1):
                price_per_kg = item['price'] / item['weight']
                print(f"{item['product']:<30} {item['price']:<10.2f} {item['weight']:<10.2f} {price_per_kg:<10.2f} {item['file']:<20}")
            print("-" * 80)
        else:
            print("Товары не найдены.")

    def save_to_html(self, results, filename='output.html'):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('<!DOCTYPE html>\n')
            f.write('<html>\n')
            f.write('<head>\n')
            f.write('<title>Результаты поиска</title>\n')
            f.write('</head>\n')
            f.write('<body>\n')
            f.write('<h1>Найденные товары</h1>\n')
            f.write('<table border="1">\n')
            f.write('<tr>\n')
            f.write('<th>Название</th>\n')
            f.write('<th>Цена</th>\n')
            f.write('<th>Вес (кг)</th>\n')
            f.write('<th>Цена/кг</th>\n')
            f.write('<th>Файл</th>\n')
            f.write('</tr>\n')
            for item in results:
                price_per_kg = item['price'] / item['weight']
                f.write('<tr>\n')
                f.write(f'<td>{html.escape(item["product"])}</td>\n')
                f.write(f'<td>{item["price"]:.2f}</td>\n')
                f.write(f'<td>{item["weight"]:.2f}</td>\n')
                f.write(f'<td>{price_per_kg:.2f}</td>\n')
                f.write(f'<td>{item["file"]}</td>\n')
                f.write('</tr>\n')
            f.write('</table>\n')
            f.write('</body>\n')
            f.write('</html>\n')


if __name__ == "__main__":
    pm = PriceMachine()
    pm.load_prices('C:\\prakt\\pythonProject\\trabota')

    while True:
        search_term = input("Введите текст для поиска (или 'exit' для выхода): ")
        if search_term.lower() == 'exit':
            print("Работа закончена.")
            break
        else:
            results = pm.find_products(search_term)
            pm.print_results(results)

            save_to_html = input("Сохранить ли ваши результаты в HTML-файл? (Да / Нет): ")
            if save_to_html.lower() == 'да':
                pm.save_to_html(results)
                print("Результаты сохранены в файл output.html")