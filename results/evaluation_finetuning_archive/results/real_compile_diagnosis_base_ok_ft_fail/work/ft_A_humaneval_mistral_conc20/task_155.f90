program main
  implicit none
  integer :: num
  integer :: even_count, odd_count
  integer, dimension(2) :: result

  ! Read input
  read(*,*) num

  ! Call the function
  call even_odd_count(num, result)

  ! Output the result
  print *, result(1), result(2)

contains

  subroutine even_odd_count(num, result)
    implicit none
    integer, intent(in) :: num
    integer, intent(out) :: result(2)
    integer :: i, digit, abs_num
    integer :: even_cnt, odd_cnt
    character(len=10) :: str

    abs_num = abs(num)
    even_cnt = 0
    odd_cnt = 0

    if (abs_num == 0) then
      result(1) = 1
      result(2) = 0
    else
      write(str, '(i0)') abs_num
      do i = 1, len_trim(str)
        digit = iachar(str(i:i)) - iachar('0')
        if (mod(digit, 2) == 0) then
          even_cnt = even_cnt + 1
        else
          odd_cnt = odd_cnt + 1
        end if
      end do
      result(1) = even_cnt
      result(2) = odd_cnt
    end if
  end subroutine even_odd_count

end program main