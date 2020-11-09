# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Tests for ExtractVolumePatches gradient."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import parameterized
import numpy as np

from tensorflow.python.eager import context
from tensorflow.python.framework import constant_op
from tensorflow.python.framework import dtypes
from tensorflow.python.framework import random_seed as random_seed_lib
from tensorflow.python.framework import test_util
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import gradient_checker
from tensorflow.python.ops import variables
from tensorflow.python.platform import test


class ExtractVolumePatchesGradTest(test.TestCase, parameterized.TestCase):
  """Gradient-checking for ExtractVolumePatches op."""

  @parameterized.parameters([
      {
          'in_shape': [2, 5, 5, 5, 3],
          'ksizes': [1, 1, 1, 1, 1],
          'strides': [1, 2, 3, 4, 1],
      },
      {
          'in_shape': [2, 7, 7, 7, 3],
          'ksizes': [1, 3, 3, 3, 1],
          'strides': [1, 1, 1, 1, 1],
      },
      {
          'in_shape': [2, 5, 7, 6, 3],
          'ksizes': [1, 3, 2, 2, 1],
          'strides': [1, 1, 1, 1, 1],
      },
      {
          'in_shape': [2, 7, 8, 6, 3],
          'ksizes': [1, 2, 3, 2, 1],
          'strides': [1, 2, 4, 3, 1],
      },
  ])
  @test_util.run_deprecated_v1
  def testGradient(self, in_shape, ksizes, strides):
    # Set graph seed for determinism.
    random_seed = 42
    random_seed_lib.set_random_seed(random_seed)

    with self.cached_session():
      np.random.seed(random_seed)
      in_val = constant_op.constant(
          np.random.random(in_shape), dtype=dtypes.float32)

      for padding in ['VALID', 'SAME']:
        out_val = array_ops.extract_volume_patches(
            in_val, ksizes, strides, padding)
        out_shape = out_val.get_shape().as_list()

        err = gradient_checker.compute_gradient_error(in_val, in_shape,
                                                      out_val, out_shape)

        print('extract_volume_patches gradient err: %.4e' % err)
        self.assertLess(err, 1e-4)

  @parameterized.parameters(set((True, context.executing_eagerly())))
  def testConstructGradientWithLargeVolumes(self, use_tape):
    with test_util.AbstractGradientTape(use_tape=use_tape) as tape:
      batch_size = 4
      planes = 8
      height = 32
      width = 32
      ksize = 5
      shape = (batch_size, planes, height, width, 1)

      volumes = variables.Variable(
          np.random.uniform(size=np.prod(shape)).reshape(shape), name='inputs')

      tape.watch(volumes)
      patches = array_ops.extract_volume_patches(
          volumes,
          ksizes=[1, ksize, ksize, ksize, 1],
          strides=[1, 1, 1, 1, 1],
          padding='SAME')
      # Github issue: #20146
      # tf.extract_volume_patches() gradient very slow at graph construction
      # time.
      gradients = tape.gradient(patches, volumes)
      # Won't time out.
      self.assertIsNotNone(gradients)


if __name__ == '__main__':
  test.main()
