The previous repository structure can be found <a href="https://github.com/0xMaka/w3py/tree/archive">here</a>

---

<img src="misc/makas_py_on_chain.png">

---

Hi! Originally this repo started as a bunch of _scripts and examples,_ written for users while handling support queries as a contributor at Sushiswap. However the repository had grown to encompass many more protocols and areas of defi, as well as outgrowing its initial lack of structure.

To make it easier to find things that might be useful, as well to know which related scripts are worth skimming through. I have attempted to better organise into folders, adding an index with short descriptions.

Always love to hear which examples can been useful, and am often happy to take requests if you might be struggling with something.
Can find me in the ethereum python discord with any questions.
All the best on your journey. - Maka

- [Ethereum Python Community](https://discord.gg/J8XFujprRA)

---

| folder                          | script                                                                         | description                                                  |
|---------------------------------|--------------------------------------------------------------------------------|--------------------------------------------------------------|
| > [ aave       ]( aave/      )  |                                                                                | **Aave lending protocol**                                    |
|                                 |  [ v3_supply_and_withdraw.py     ]( aave/v3_supply_and_withdraw.py           ) | Approve, supply and withdraw from a v3 aave pool.            |
| > [ beraswap   ]( beraswap/  )  |                                                                                | **Berachain DEX**                                            |
|                                 |  [ bera_swap.py                  ]( beraswap/bera_swap.py                    ) | Swap using `batchSwap` with their `ERC20_DEX`.               | 
| > [ flashbots  ]( flashbots/ )  |                                                                                | Call structures and direct calls to flashbots endpoints.     |
|                                 |  [ eth_send_bundle.py            ]( flashbots/eth_send_bundle.py             ) | Building and sending a classic bundle.                       |
|                                 |  [ eth_send_private.py           ]( flashbots/eth_send_private.py            ) | Using Flashbots endpoint to send a private transaction.      | 
|                                 |  [ mev_send_bundle.py            ]( flashbots/mev_send_bundle.py             ) | Building and sending a classic bundle.                       |     
| > [ general    ]( general    )  |                                                                                | **Overrides, bloom filters, log topics and wider EVM**       |
|                                 |  [ bloom_filter.py               ]( general/bloom_filter.py                  ) | Filtering the `logsBloom` for more efficient searches.       |
|                                 |  [ multi2.py                     ]( general/multi2.py                        ) | Using a popular mulicall contract, to batch static requests. |
|                                 |  [ swap_topic.py                 ]( general/swap_topic.py                    ) | How to encode and pull a `Event` topic.                      |
|                                 |  [ transfer_override.py          ]( general/transfer_override.py             ) | Overiding an accounts ERC20 balance, prior to an `eth_call`. |
| > [ raw_calls  ]( raw_calls/ )  |  [                               ](                                          ) | **Contract calls sending raw calldata**                      |
|                                 |  [ raw_approval.py               ]( raw_calls/raw_approval.py                ) | Send a token approval using pre prepared calldata.           |
|                                 |  [ raw_deploy.py                 ]( raw_calls/raw_deploy.py                  ) | Deploy a contract using pre prepared calldata.               |
|                                 |  [ raw_deposit.py                ]( raw_calls/raw_deposit.py                 ) | Deposit ETH to receive WETH using pre prepared calldata.     |
|                                 |  [ raw_transfer.py               ]( raw_calls/raw_transfer.py                ) | Make an ERC20 transfer using pre prepared calldata.          |
| > [ scrap_bots ]( scrap_bots/)  |                                                                                | **Basic bot flow**                                           |
|                                 |  [ skym_bot/                     ]( scrap_bots/skym_bot/                     ) | Monitor a v2 pair for imbalance, skim with contract if so.   |
|                                 |  [ flash_bot.py                  ]( scrap_bots/flash_bot.py                  ) | A basic flashbot script, using flashbots py library.         |
|                                 |  [ voly.py                       ]( scrap_bots/voly.py                       ) | Polls a v2 pair for price, buys or sells, tracks if holding. |
| > [ signing    ]( signing/   )  |                                                                                | **Offchain signing, permits, EIP712**                        |
|                                 |  [ pysign.py                     ]( signing/pysign.py                        ) | Deprectated signing pattern.                                 |
|                                 |  [ setMasterContractApproval.py  ]( signing/setMasterContractApproval.py     ) | Building and signing an EIP712 digest.                       |
|                                 |  [ universal_permit2_extended.py ]( signing/universal_permit2_extended.py    ) | Building an offchain permit for Universal router (long way). |
| > [ sushiswap  ]( sushiswap/ )  |                                                                                | **Sushi specific**                                           |
|                                 |  [ exact_input.py                ]( sushiswap/exact_input.py                 ) | Trident single hop swap.                                     |
|                                 |  [ get_kava_farms.py             ]( sushiswap/get_kava_farms.py              ) | Get a list of all farms from a chef.                         |
|                                 |  [ get_rewards.py                ]( sushiswap/get_rewards.py                 ) | Calculating rewards from a Minichef.                         |
|                                 |  [ graph_call.py                 ]( sushiswap/graph_call.py                  ) | Outdated: Exchange subgraph call (Pre needing a key).        |
|                                 |  [ route_processor.md            ]( sushiswap/route_processor.md             ) | Notes Sushi's router processor.                              |
|                                 |  [ route_processor.py            ]( sushiswap/route_processor.py             ) | Single hop swap using Sushi route processor.                 |
|                                 |  [ route_processor_multi.py      ]( sushiswap/route_processor_multi.py       ) | Multi hop swap using Sushi route processor.                  |
|                                 |  [ swap_volume_since_midnight.py ]( sushiswap/swap_volume_since_midnight.py  ) | Outdated: Use a subgraph to get volume day data.             |
|                                 |  [ trident_help_sheet.md         ]( sushiswap/trident_help_sheet.md          ) | Notes on Sushi Trident.                                      |
|                                 |  [ trident_multicall.py          ]( sushiswap/trident_multicall.py           ) | Trident multi hop swap.                                      |
|                                 |  [ xSwap.py                      ]( sushiswap/xSwap.py                       ) | Extensive cross chain swap, encoding, off chain signing etc. |
| > [ syncswap   ]( syncswap/  )  |                                                                                | **How to swap on Syncwap DEX.**                              |
|                                 |  [ sync_swap.py                  ]( syncswap/sync_swap.py                    ) | Basic syncswap router interaction.                           |
|                                 |  [ sync_swap_with_permit.py      ]( syncswap/sync_swap_with_permit.py        ) | Basic syncswap router interaction using a permit.            |
| > [ uniswapv2  ]( uniswapv2/ )  |                                                                                | **Examples for Uniswap v2 and clones**                       |
|                                 |  [ mempool_filter.py             ]( uniswapv2/mempool_filter.py              ) | IPC filter the tx pool for swaps and decode them.            |
|                                 |  [ scale4whale.py                ]( uniswapv2/scale4whale.py                 ) | Get an amount required to buy a tokens total supply.         |
|                                 |  [ v2path_encode.md              ]( uniswapv2/v2path_encode.md               ) | Step through of the ABI encoding.                            |
| > [ uniswapv3  ]( uniswapv3/ )  |                                                                                | **Examples for Uniswap v3 and clones**                       |
|                                 |  [ v3exactOutput.py              ]( uniswapv3/v3exactOutput.py               ) | Uniswap v3 swap, multihop.                                   |
|                                 |  [ v3exactOutputSingle.py        ]( uniswapv3/v3exactOutputSingle.py         ) | Uniswap v3 swap, single hop.                                 |
|                                 |  [ v3quoter_iterations.py        ]( uniswapv3/v3quoter_iterations.py         ) | Uniswap v3 quoter discrepancies, example calls to each.      |
| > [ uni_router ]( uni_router/)  |                                                                                | **Uniswaps Universal router**                                |
|                                 |  [ universal_router_swap.md      ]( uni_router/universal_router_swap.md      ) | Notes on Uniswaps Universal Router.                          |
|                                 |  [ universal_router_swap.py      ]( uni_router/universal_router_swap.py      ) | Wrap and swap from Eth using Universal router..              |
|                                 |  [ universal_swap_from_token.py  ]( uni_router/universal_swap_from_token.py  ) | Swap from token using Universal router (uses dual tx permit).|
| > [ zk         ]( zk/        )  |                                                                                | **Anything ZK specific**                                     |
|                                 |  [ check_balance.py              ]( zk/check_balance.py                      ) | Simple balance check, using the sdk.                         |
|                                 |  [ transfer.py                   ]( zk/transfer.py                           ) | Simple eth transfer, using the sdk.                          |
|         <img width=145/>        |                                                                                |                     <img width=430/>                         |

<!--
<table class="fixed-align">
  <tbody>
   <tr>
  <th>
    🐍
  </th>
    </tr>  
    <tr>
  <td valign="top", valign="center">
     
```python
# clone repo 
# ...
# instructions for using search tag tool
# ...
``` 

  </td>
    </tr>
  <tr>
<td>
  <img width=800/>
</td>
  </tr>
</table>
