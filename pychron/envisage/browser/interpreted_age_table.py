# ===============================================================================
# Copyright 2013 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

# ============= enthought library imports =======================
from traits.api import List, Any, Bool, Event, Instance
# ============= standard library imports ========================
# ============= local library imports  ==========================
from pychron.column_sorter_mixin import ColumnSorterMixin
from pychron.envisage.browser.adapters import InterpretedAgeAdapter


def sort_items(ans):
    return sorted(ans, key=lambda x: x.timestampf)


class InterpretedAgeTable(ColumnSorterMixin):
    interpreted_ages = List
    ointerpreted_ages = List
    selected = Any
    dclicked = Any

    context_menu_event = Event
    #
    # analysis_filter = CStr
    # analysis_filter_values = List
    # analysis_filter_comparator = Enum('=', '<', '>', '>=', '<=', 'not =', 'startswith')
    # analysis_filter_parameter = Str
    # analysis_filter_parameters = Property(List, depends_on='tabular_adapter.columns')

    # omit_invalid = Bool(True)
    # table_configurer = Instance(AnalysisTableConfigurer)
    #
    # limit = DelegatesTo('table_configurer')
    # omit_invalid = DelegatesTo('table_configurer')

    no_update = False
    scroll_to_row = Event
    refresh_needed = Event
    tabular_adapter = Instance(InterpretedAgeAdapter)
    append_replace_enabled = Bool(True)

    # def add_analyses(self, ans):
    #     items = self.analyses
    #     items.extend(ans)
    #     self.oanalyses = self.analyses = sort_items(items)
    #
    # def set_analyses(self, ans, tc=None, page=None, reset_page=False, selected_identifiers=None):
    #     if selected_identifiers:
    #         aa = self.analyses
    #         aa = [ai for ai in aa if ai.identifier in selected_identifiers]
    #         aa.extend(ans)
    #     else:
    #         aa = ans
    #
    #     self.oanalyses = self.analyses = sort_items(aa)

    # def configure_table(self):
    #     self.table_configurer.edit_traits(kind='livemodal')
    def set_interpreted_ages(self, ias):
        self.interpreted_ages = self.ointerpreted_ages = ias
        # self.oanalyses = self.analyses = sort_items(ias)

    # handlers
    def _interpreted_ages_items_changed(self, old, new):
        if self.sort_suppress:
            return

        if new.removed:
            for ai in new.removed:
                self.ointerpreted_ages.remove(ai)

    # def _analysis_filter_changed(self, new):
    #     if new:
    #         name = self.analysis_filter_parameter
    #         self.analyses = fuzzyfinder(new, self.oanalyses, name)
    #         # self.analyses = filter(filter_func(new, name), self.oanalyses)
    #     else:
    #         self.analyses = self.oanalyses
    #
    # def _analysis_filter_comparator_changed(self):
    #     self._analysis_filter_changed(self.analysis_filter)
    #
    # # def _analysis_filter_parameter_changed(self, new):
    # #     if new:
    # #         vs = []
    # #         p = self._get_analysis_filter_parameter()
    # #         for si in self.oanalyses:
    # #             v = getattr(si, p)
    # #             if v not in vs:
    # #                 vs.append(v)
    # #
    # #         self.analysis_filter_values = vs
    #
    # def _get_analysis_filter_parameter(self):
    #     p = self.analysis_filter_parameter
    #     return p.lower()
    #
    # @cached_property
    # def _get_analysis_filter_parameters(self):
    #     return dict([(ci[1], ci[0]) for ci in self.tabular_adapter.columns])
    #
    # # defaults
    # def _table_configurer_default(self):
    #     return AnalysisTableConfigurer(id='analysis.table',
    #                                    title='Configure Analysis Table')
    #
    # def _analysis_filter_parameter_default(self):
    #     return 'record_id'

    def _tabular_adapter_default(self):
        # adapter = AnalysisAdapter()
        # self.table_configurer.adapter = adapter
        # self.table_configurer.load()
        adapter = InterpretedAgeAdapter()
        return adapter

# ============= EOF =============================================
