## Notes
This is a golang implementation of Many-Time-Pad attack. The encrypted messages are stored in `encrypt.txt` where the first 10 items are encrypted by 
a same key. I use these items to decrypt the 11th items.  
TODO: the attack principle

## Test
```bash
cd cmd/

./attack
```
### Result
```
The secuet mes*age*is* Whtn using aa*tream cipher**never*use the key more than once
```