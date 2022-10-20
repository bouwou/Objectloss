package com.example.myapplication.adapter

import android.annotation.SuppressLint
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.cardview.widget.CardView
import androidx.navigation.findNavController
import androidx.recyclerview.widget.RecyclerView
import com.example.myapplication.R
import com.example.myapplication.model.ObjectClass

class ObjectListAdapter(
    var dataSet: List<ObjectClass>,
    /*var uploadSelectItemImpl: UploadSelectItemImpl,*/
    /*var textViewTotalPanier:TextView*/
) :
    RecyclerView.Adapter<ObjectListAdapter.ViewHolder>() {

    lateinit var listdataSearch: MutableList<ObjectClass>
    private var counter: Int = 0

    init {
        listdataSearch = ArrayList()
        listdataSearch.addAll(dataSet)
    }

    // Create new views (invoked by the layout manager)
    override fun onCreateViewHolder(viewGroup: ViewGroup, viewType: Int): ViewHolder {
        // Create a new view, which defines the UI of the list item
        val view = LayoutInflater.from(viewGroup.context)
            .inflate(R.layout.item_objet, viewGroup, false)
        return ViewHolder(view)
    }

    var row_index = -1

    @SuppressLint("ResourceAsColor")
    override fun onBindViewHolder(viewHolder: ViewHolder, position: Int) {
//        viewHolder.textViewCartItem.text = listdataSearch[position].menus!!.name
        viewHolder.cardItemObject.setOnClickListener{ v ->
            onClick(
                v,
                position
            )
        }
    }

    private fun onClick(v: View?, position: Int) {
//        val infoCart = bundleOf("infoCart" to Gson().toJson(listdataSearch[position]))
         v?.findNavController()
             ?.navigate(R.id.action_nav_object_list_to_customerObjectLDetailFragment)
//        var intent = Intent(v!!.context,CartActivity::class.java)
//        v.startstartActivity(intent)

    }

    // Return the size of your dataset (invoked by the layout manager)
    override fun getItemCount() = listdataSearch.size

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val cardItemObject: CardView
        val textViewNumber: TextView
        val textViewProprietaire: TextView
        val textViewDate: TextView
        val textViewType: TextView
        val textViewStatusCard: CardView
        val textViewStatusName: TextView

        init {
            cardItemObject = view.findViewById(R.id.cardItemObject)
            textViewNumber = view.findViewById(R.id.textViewNumber)
            textViewProprietaire = view.findViewById(R.id.textViewProprietaire)
            textViewDate = view.findViewById(R.id.textViewDate)
            textViewType = view.findViewById(R.id.textViewType)
            textViewStatusCard = view.findViewById(R.id.textViewStatusCard)
            textViewStatusName = view.findViewById(R.id.textViewStatusName)
        }

    }


}