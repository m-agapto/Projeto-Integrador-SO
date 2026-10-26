# Exemplo demonstrativo: mostra a data/hora e o espaço livre na unidade atual.
Get-Date
Get-PSDrive -PSProvider FileSystem | Select-Object Name, Used, Free
