## Streaming Strategy

Problem: 5GB files crash if loaded into memory
Solution:

* HTTP chunked read from S3 (8KB pieces)
* Line-by-line JSON parsing (buffer management)
* Process on-the-fly

Result: Analyze 1000 records in ~0.3s using ~10MB RAM instead of 5GB