"""
Created on Thu Oct 29 08:43 2019

@author: Superkmi
"""

from time import time
from flask import Flask,jsonify,request
import json,hashlib

app = Flask(__name__)

class BlockChain(object):
    def __init__(self):
        # 区块信息存储
        self.blockChain = []
        # 一个区块中有多笔交易数据，存储交易数据
        self.current_transactions = []
        # 创始区块
        self.new_block()

    def get_block_hash(self,block):
        block_str = json.dumps(block,sort_keys=True).encode('UTF-8') # 加密时需要设置编码
        return hashlib.sha256(block_str).hexdigest()

    # 创建区块的方法
    def new_block(self):
        # 区块
        block = {
            'index' : len(self.blockChain),
            'timestramp' : time(),
            'transaction' : self.current_transactions,
            'nonce' : -1,
            'pre_hash' : None if len(self.blockChain) == 0 else self.get_block_hash(self.blockChain[-1])
        }
        # 挖矿的过程就是通过Nonce去匹配符合条件的hash
        hash = None
        while not self.valid_proot(hash,4):
            block['nonce'] += 1
            hash = self.get_block_hash(block)

        # 添加到区块链
        self.blockChain.append(block)
        # 清除交易列表
        self.current_transactions = []
        return block

    # 获取前端交易信息
    def new_transaction(self,sender,receive,amount):
        self.current_transactions.append(
            {
                'sender' : sender,
                'receive' : receive,
                'amount' : amount
            }
        )
    # 判断当前生成的hash是否满足系统指定的难度
    def valid_proot(self,hash,dct):
        return False if hash is None else hash[:dct] == '0000'

if __name__ == '__main__':
    blockchain = BlockChain()

    @app.route('/mine', methods=['get', 'post'])
    def mine():
        # 返回当前生成的区块
        return jsonify(blockchain.new_block())

    @app.route('/chain', methods=['get', 'post'])
    def full_chain():
        rst = {
            'length' : len(blockchain.blockChain),
            'chain' : blockchain.blockChain,
        }
        return jsonify(rst)

    @app.route('/trans',methods=['get','post'])
    def trans_form():
        html = '''
        <form action="/trans" method="post">
        from:<input name="sender"><br/>
        to:<input name="receiver"><br/>
        amount:<input name="amount"><br/>
        <button type="submit">trans</button>
        </form>
        '''
        return html


    @app.route('/trans', methods=['post'])
    def add_transaction():
        sender = request.form['sender']
        receiver = request.form['receiver']
        amount = request.form['amount']

        blockchain.new_transaction(sender,receiver,amount)

        return '添加成功!'

    app.run(debug=False)