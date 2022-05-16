import asyncio
import time



async def me():
    print('i''m a corutin')

async def hello_word():
    print('frist hello world')
    await asyncio.sleep(2)
    print('second hello world')
    await asyncio.sleep(1)
    print('three hello world')


async def main():

   
      
    await asyncio.gather(
        hello_word(),
        hello_word()
    )



if __name__ == '__main__':

    asyncio.run(main())