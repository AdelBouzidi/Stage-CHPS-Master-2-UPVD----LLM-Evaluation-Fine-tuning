program smallest_change_demo
  implicit none
  integer, parameter :: arr_len = 8
  integer, dimension(arr_len) :: arr
  integer :: i

  ! Initialize array with example values
  arr = [1, 2, 3, 5, 4, 7, 9, 6]

  ! Call the function
  print *, 'Smallest change:', smallest_change(arr_len, arr)

contains

  function smallest_change(arr_len, arr) result(res)
    integer, intent(in) :: arr_len
    integer, intent(in) :: arr(:)
    integer :: res
    integer :: i
    
    res = 0
    do i = 1, arr_len / 2
      if (arr(i) /= arr(arr_len - i + 1)) then
        res = res + 1
      end if
    end do
  end function smallest_change

end program smallest_change_demo