def deleteDups(entry):
    # Creamos una lista nueva para guardar los elementos únicos
    result = []
    
    # Primer loop: recorre cada elemento de la lista original
    for i in range(len(entry)):
        dup = False
        
        # Segundo loop: compara el elemento actual con los que ya guardamos en 'result'
        for j in range(len(result)):
            if entry[i] == result[j]:
                dup = True
                break  # Si ya lo encontramos, no hace falta seguir comparando
        
        # Si después de revisar todo 'result' no estaba, lo agregamos
        if not dup:
            result.append(entry[i])
            
    return result

def quick_sort(arr):
    # Caso base: si el array tiene 0 o 1 elementos, ya está ordenado
    if len(arr) <= 1:
        return arr
    
    # Seleccionamos el elemento central como el pivot
    pivot = arr[len(arr) // 2]
    
    # Partición del array en tres partes
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    # Recursión: ordenamos las partes y las concatenamos
    return quick_sort(left) + middle + quick_sort(right)

entry = [4,2,7,2,4,9,1]
print(f"Original {entry}")
entry2 = deleteDups(entry)
print(f"Sin duplicados {entry2}")
entry3 = quick_sort(entry2)
print(f"Menor a mayor {entry3}")