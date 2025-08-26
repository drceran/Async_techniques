from multiprocessing.pool import Pool

pool = Pool(processes= 4)

pool.apply_async(func=do_math, args = (0,100))

pool.apply_async(func=do_math, args = (101,200))

pool.apply_async(func=do_math, args = (201,201))

pool.apply_async(func=do_math, args = (301,4400))

pool.close()

pool.join()