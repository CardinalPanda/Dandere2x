//
// Created by tyler on 02/03/2021.
//

#ifndef CPP_REWORK_FRAME_UTILITIES_H
#define CPP_REWORK_FRAME_UTILITIES_H

#include "Frame.h"

class FrameUtilities{
public:

    static void copy_frame_using_blocks(Frame &final_frame,
                                         const Frame &base_image,
                                         const vector<vector<shared_ptr<Block>>>& matched_blocks,
                                         const int block_size){
        for (const vector<shared_ptr<Block>>& row: matched_blocks){

            for (const shared_ptr<Block>& block: row) {
                if (block == nullptr)
                    continue;

                for (int i = 0; i < block_size; i++) {
                    for (int j = 0; j < block_size; j++) {
                        final_frame.set_color(block->x_end + i, block->y_end + j,
                                              base_image.get_color(block->x_start + i, block->y_start + j));
                    }
                }
            }
        }

    }
};

#endif //CPP_REWORK_FRAME_UTILITIES_H