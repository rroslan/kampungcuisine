# Kampungcuisine Database Population Summary

This document summarizes the categories and products that have been populated in the kampungcuisine Django project.

## Categories

The following three categories have been created:

### 1. Ready to Eat
**Description:** Delicious pre-cooked Malaysian dishes ready to serve

### 2. Spice Paste
**Description:** Authentic Malaysian spice pastes for cooking

### 3. Spice Blend
**Description:** Traditional Malaysian spice blends and seasonings

## Products by Category

### Ready to Eat (5 products)

1. **Rendang Daging** (RTE-REN-001) - RM18.90
   - Traditional Minangkabau slow-cooked beef in rich coconut curry. Tender beef chunks in aromatic spices.

2. **Curry Chicken** (RTE-CUR-001) - RM15.90
   - Malaysian-style curry chicken with potatoes in coconut milk and spices.

3. **Beef Curry** (RTE-CUR-002) - RM19.90
   - Rich and flavorful beef curry with tender meat in aromatic curry sauce.

4. **Ayam Masak Merah** (RTE-AMM-001) - RM16.90
   - Chicken cooked in spicy tomato-based sauce with onions and chili.

5. **Sambal Udang** (RTE-SAM-001) - RM22.90
   - Fresh prawns cooked in spicy sambal sauce with tamarind and chili.

### Spice Paste (5 products)

1. **Rendang Paste** (SPA-REN-001) - RM8.90
   - Authentic rendang spice paste made with galangal, lemongrass, chili, and traditional spices.

2. **Curry Paste** (SPA-CUR-001) - RM7.90
   - Traditional Malaysian curry paste with coconut, chili, and aromatic spices.

3. **Sambal Paste** (SPA-SAM-001) - RM6.90
   - Fiery sambal paste made with fresh chilies, shallots, and belacan.

4. **Laksa Paste** (SPA-LAK-001) - RM9.90
   - Aromatic laksa spice paste for authentic Malaysian laksa noodle soup.

5. **Tom Yam Paste** (SPA-TOM-001) - RM8.50
   - Spicy and sour tom yam paste with lemongrass, galangal, and lime leaves.

### Spice Blend (6 products)

1. **Rendang Spice Blend** (SPB-REN-001) - RM5.90
   - Dry spice blend for rendang with coriander, cumin, fennel, and other traditional spices.

2. **Curry Powder** (SPB-CUR-001) - RM4.90
   - Malaysian curry powder blend with turmeric, coriander, cumin, and chili.

3. **Fish Curry Powder** (SPB-FIS-001) - RM5.50
   - Special spice blend for fish curry with fennel, coriander, and aromatic spices.

4. **Meat Curry Powder** (SPB-MEA-001) - RM6.50
   - Robust spice blend for meat curry with star anise, cardamom, and traditional spices.

5. **Garam Masala** (SPB-GAR-001) - RM7.90
   - Traditional garam masala blend with cinnamon, cardamom, cloves, and black pepper.

6. **Biryani Spice Mix** (SPB-BIR-001) - RM9.50
   - Aromatic spice mix for biryani with saffron, bay leaves, and exotic spices.

## Database Statistics

- **Total Categories:** 3
- **Total Products:** 16
- **All products are published and available**

## SKU Convention

The SKU (Stock Keeping Unit) follows this pattern:
- **RTE-XXX-001:** Ready to Eat products
- **SPA-XXX-001:** Spice Paste products  
- **SPB-XXX-001:** Spice Blend products

Where XXX is a 3-letter abbreviation of the product name.

## Management Command

To populate the database with this data, run:
```bash
python manage.py populate_kampungcuisine --settings=core.settings_dev
```

## Notes

- All products have unique SKUs and slugs
- Prices are in Malaysian Ringgit (RM)
- All products are marked as published (`is_published=True`)
- Categories have auto-generated slugs based on their names
- The data focuses on authentic Malaysian cuisine products