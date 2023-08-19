from bs4 import BeautifulSoup
import csv

# HTML table code snippet
html_table = '''<table class="f1-award-table">
  <tbody><tr>
    <th class="align-center">Pos.</th>
    <th>Team</th>
    <th>Driver</th>
    <th>Time (sec)</th>
    <th>Lap</th>
    <th>Points</th>
  </tr>
      <tr>
      <td class="align-center"><strong>1</strong></td>
      <td>Red Bull</td>
      <td>Perez</td>
      <td>2.11</td>
      <td>1</td>
      <td><strong>25</strong></td>
    </tr>
      <tr>
      <td class="align-center"><strong>2</strong></td>
      <td>Red Bull</td>
      <td>Perez</td>
      <td>2.62</td>
      <td>2</td>
      <td><strong></strong></td>
    </tr>
      <tr>
      <td class="align-center"><strong>3</strong></td>
      <td>Alpine</td>
      <td>Ocon</td>
      <td>2.65</td>
      <td>1</td>
      <td><strong>18</strong></td>
    </tr>
      <tr>
      <td class="align-center"><strong>4</strong></td>
      <td>Ferrari</td>
      <td>Sainz</td>
      <td>2.71</td>
      <td>7</td>
      <td><strong>15</strong></td>
    </tr>
      <tr>
      <td class="align-center"><strong>5</strong></td>
      <td>Williams</td>
      <td>Sargeant</td>
      <td>2.93</td>
      <td>1</td>
      <td><strong>12</strong></td>
    </tr>
      <tr>
      <td class="align-center"><strong>6</strong></td>
      <td>AlphaTauri</td>
      <td>De Vries</td>
      <td>2.94</td>
      <td>45</td>
      <td><strong>10</strong></td>
    </tr>
      <tr>
      <td class="align-center"><strong>7</strong></td>
      <td>Williams</td>
      <td>Sargeant</td>
      <td>2.98</td>
      <td>2</td>
      <td><strong></strong></td>
    </tr>
      <tr>
      <td class="align-center"><strong>8</strong></td>
      <td>AlphaTauri</td>
      <td>Tsunoda</td>
      <td>2.99</td>
      <td>54</td>
      <td><strong>8</strong></td>
    </tr>
      <tr>
      <td class="align-center"><strong>9</strong></td>
      <td>Alfa Romeo</td>
      <td>Zhou</td>
      <td>3.37</td>
      <td>1</td>
      <td><strong>6</strong></td>
    </tr>
      <tr>
      <td class="align-center"><strong>10</strong></td>
      <td>Williams</td>
      <td>Sargeant</td>
      <td>3.63</td>
      <td>36</td>
      <td><strong></strong></td>
    </tr>
      <tr>
      <td class="align-center"><strong>11</strong></td>
      <td>Alfa Romeo</td>
      <td>Bottas</td>
      <td>3.65</td>
      <td>1</td>
      <td><strong>4</strong></td>
    </tr>
      <tr>
      <td class="align-center"><strong>12</strong></td>
      <td>Mercedes</td>
      <td>Russell</td>
      <td>3.69</td>
      <td>7</td>
      <td><strong>2</strong></td>
    </tr>
      <tr>
      <td class="align-center"><strong>13</strong></td>
      <td>McLaren</td>
      <td>Piastri</td>
      <td>3.96</td>
      <td>54</td>
      <td><strong>1</strong></td>
    </tr>
      <tr>
      <td class="align-center"><strong>14</strong></td>
      <td>Alfa Romeo</td>
      <td>Bottas</td>
      <td>4.31</td>
      <td>53</td>
      <td><strong></strong></td>
    </tr>
      <tr>
      <td class="align-center"><strong>15</strong></td>
      <td>Haas</td>
      <td>Magnussen</td>
      <td>5.48</td>
      <td>7</td>
      <td><strong></strong></td>
    </tr>
      <tr>
      <td class="align-center"><strong>16</strong></td>
      <td>Alfa Romeo</td>
      <td>Zhou</td>
      <td>6.90</td>
      <td>54</td>
      <td><strong></strong></td>
    </tr>
  </tbody></table>
'''

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(html_table, 'html.parser')

# Extract table rows
table_rows = soup.find_all('tr')

# Create a CSV file
csv_filename = 'data_Pitstops/Australian.csv'


with open(csv_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Write table rows to CSV
    for row in table_rows:
        csvwriter.writerow([cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])])

print(f'CSV file saved as {csv_filename}')
