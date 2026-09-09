program palindrome_change
  implicit none
  integer, parameter :: max_len = 100
  integer :: arr_len
  integer, dimension(max_len) :: arr
  integer :: result

  ! Read input
  read(*,*) arr_len
  read(*,*) arr(1:arr_len)

  ! Calculate minimum changes needed
  result = smallest_change(arr_len, arr)

  ! Output result
  print *, result

contains

  integer function smallest_change(arr_len, arr)
    integer, intent(in) :: arr_len
    integer, intent(in) :: arr(max_len)
    integer :: i, j, changes
    changes = 0
    i = 1
    j = arr_len
    do while (i < j)
      if (arr(i) /= arr(j)) then
        changes = changes + 1
      end if
      i = i + 1
      j = j - 1
    end do
    smallest_change = changes
  end function smallest_change

end program palindrome_change