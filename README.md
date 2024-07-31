# **Blockchain Simulator**
**Performance testing of blockchain network**

### Notice
*The code repository is part of a master's thesis in Telecommunications (ICT & Cybersecurity) done at the Warsaw University of Technology. The Master of Science (MSc) degree was awarded in September 2023.*

## Description
The success of networks such as Bitcoin, or Ethereum has contributed to the widespread use of blockchain technology in the financial industry (in the form of cryptocurrencies). Today, the technology is picking up new areas, finding use in the logistics, medical, and insurance industries, among others.

One of the most desirable features of a blockchain network is high performance (scalability), i.e. the ability to transfer and store as much data as possible in the shortest possible time, but without compromising the core assumptions of the network, such as decentralization or security. Nevertheless, the detailed impact of network parameters on its performance has not been sufficiently analyzed due to their large number and variability. Many blockchain networks have different usages, structures and consensus algorithms, making it a complicated task to analyze the impact of each of these parameters on the performance. In addition, blockchain is a relatively new technology, so research is still underway to fully understand its operation and optimization. Therefore, there is a need for further research in this area.

The thesis presents an implementation of an event-driven simulator of a peer-to-peer blockchain network, and presents the results and conclusions of the network performance tests performed using it. The two investigated metrics that define network performance are the average transaction confirmation time and the number of stale blocks. When the average transaction confirmation time is high and the number of stale blocks increases, the network becomes poorly scalable, thus its usage and attractiveness decrease. The study examined how the following parameters affect the described metrics: the number of full nodes, the number of miners, the maximumblock size, the number of neighbors of a single node, and the propagation time (network latency).

The results and conclusions of the research presented in the paper, as well as the simulator itself, can be used when implementing new or optimizing existing blockchain networks, both public and private. This will allow selecting optimal parameters of the network at the design stage so that it is scalable.
