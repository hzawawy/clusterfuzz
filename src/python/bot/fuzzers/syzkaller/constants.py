# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Constants that are meaningful to syzkaller.
Should not have any dependancies.
"""

# Regex to find testcase path from a crash.
KASAN_CRASH_TESTCASE_REGEX = (r'.*Test unit written to\s*'
                              r'(Read|Write) of .*')

SYZKALLER_WORK_FOLDER = '/tmp/syzkaller'

VMLINUX_FOLDER = '/tmp/syzkaller/vmlinux'

CLEAN_EXIT_SECS = 10
